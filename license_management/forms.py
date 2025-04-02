from django import forms
from .models import License, LicenseAssignment, LicenseType
from dcim.models import Manufacturer, Device
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from .filtersets import LicenseAssignmentFilterSet, LicenseFilterSet
from virtualization.models import VirtualMachine, Cluster
from utilities.forms.rendering import FieldSet, TabbedGroups
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

from license_management import filtersets


class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    filterset_class = LicenseFilterSet

    fieldsets = (
        FieldSet('q', name='Search'),
        FieldSet('manufacturer_id', 'license_key', name='License Info'),
        FieldSet('is_parent_license', 'is_child_license', 'parent_license', 'child_license', name='License Relationship'),
        FieldSet('purchase_date_after', 'purchase_date_before', 'expiry_date_after', 'expiry_date_before', name='Dates'),
    )

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer"
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.filter(parent_license__isnull=True),
        required=False,
        label="Parent License",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    child_license = DynamicModelMultipleChoiceField(
        queryset=License.objects.filter(sub_licenses__isnull=False),
        required=False,
        label="Child Licenses",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    is_parent_license = forms.NullBooleanField(
        required=False,
        label="Is Parent License",
        widget=forms.Select(choices=[('', '---------'), (True, 'Yes'), (False, 'No')])
    )

    is_child_license = forms.NullBooleanField(
        required=False,
        label="Is Child License",
        widget=forms.Select(choices=[('', '---------'), (True, 'Yes'), (False, 'No')])
    )

    license_key = forms.CharField(
        required=False,
        label="License Key"
    )

    purchase_date_after = forms.DateField(
        required=False,
        label="Purchase Date (After)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    purchase_date_before = forms.DateField(
        required=False,
        label="Purchase Date (Before)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    expiry_date_after = forms.DateField(
        required=False,
        label="Expiry Date (After)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    expiry_date_before = forms.DateField(
        required=False,
        label="Expiry Date (Before)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class LicenseImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer'
    )

    parent_license = CSVModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        to_field_name='license_key',
        label='Parent License',
        help_text='Parent license key if applicable'
    )

    class Meta:
        model = License
        fields = [
            "license_key", "serial_number", "description",
            "manufacturer", "purchase_date", "expiry_date",
            "volume_limit", "parent_license"
        ]
        labels = {
            "license_key": "License Key",
            "serial_number": "Serial Number",
            "description": "Description",
            "manufacturer": "Manufacturer",
            "purchase_date": "Purchase Date",
            "expiry_date": "Expiry Date",
            "volume_limit": "Volume Limit",
            "parent_license": "Parent License",
        }
        help_texts = {
            "license_key": "Unique license key",
            "serial_number": "Serial number of the license",
            "description": "Additional notes or description",
            "manufacturer": "Manufacturer of the software/license",
            "purchase_date": "Date when the license was purchased",
            "expiry_date": "Expiration date of the license",
            "volume_limit": "Number of uses (if volume license)",
            "parent_license": "Link to a parent license if this is a child",
        }

    def clean(self):
        super().clean()


class LicenseBulkEditForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "description", "manufacturer", "purchase_date",
            "expiry_date", "volume_limit", "parent_license",
        ]


class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
    )

    license_type = DynamicModelChoiceField(
        queryset=LicenseType.objects.all(),
        required=True,
        label="License Type",
        help_text="Select the type of license.",
        selector=True,
        quick_add=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        help_text="Select a parent license if applicable.",
        selector=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    license_key = forms.CharField(
        required=True,
        label="License Key"
    )

    purchase_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Purchase Date"
    )

    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Expiry Date"
    )

    comment = CommentField()

    class Meta:
        model = License
        fields = [
            "manufacturer","license_type", "license_key", "serial_number", "description",
            "volume_limit", "parent_license",
            "purchase_date", "expiry_date", "comment"
        ]


class LicenseTypeForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="Manufacturer",
        selector=True,
        quick_add=True
    )

    volume_type = forms.ChoiceField(
        choices=LicenseType.VOLUME_TYPE_CHOICES,
        required=True,
        label="Volume Type"
    )

    license_model = forms.ChoiceField(
        choices=LicenseType.LICENSE_MODEL_CHOICES,
        required=True,
        label="License Model"
    )

    base_license = DynamicModelChoiceField(
        queryset=LicenseType.objects.filter(license_model="BASE"),
        required=False,
        label="Base License",
        help_text="Select a base license if this is an expansion pack.",
        selector=True
    )

    purchase_model = forms.ChoiceField(
        choices=LicenseType.PURCHASE_MODEL_CHOICES,
        required=True,
        label="Purchase Model"
    )

    slug = SlugField(
        required=True,
        label="Slug",
        help_text="URL-friendly identifier",
        slug_source="name",
    )

    comments = CommentField()

    class Meta:
        model = LicenseType
        fields = [
            "name",
            "slug",
            "manufacturer",
            "product_code",
            "ean_code",
            "volume_type",
            "license_model",
            "base_license",
            "purchase_model",
            "description",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        license_model = self.initial.get("license_model") or self.data.get("license_model")
        if license_model == "EXPANSION":
            self.fields["base_license"].required = True
        else:
            self.fields["base_license"].required = False

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data:
            return cleaned_data

        license_model = cleaned_data.get("license_model")
        base_license = cleaned_data.get("base_license")

        if license_model == "EXPANSION" and not base_license:
            self.add_error("base_license", "You must select a base license when the license model is set to 'Expansion Pack'.")

        return cleaned_data



class LicenseAssignmentForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.none(),
        required=True,
        label="License",
        selector=True,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device",
        selector=True
    )

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine",
        selector=True
    )

    comments = CommentField()

    fieldsets = (
        FieldSet("manufacturer", "license", "volume", "description", name="General Information"),
        FieldSet(
            TabbedGroups(
                FieldSet("device", name="Device Assignment"),
                FieldSet("virtual_machine", name="Virtual Machine Assignment"),
            ),
            name="Assignment Type"
        ),
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer", "license", "device", "virtual_machine",
            "volume", "description", "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        manufacturer = (
            self.data.get("manufacturer")
            or self.initial.get("manufacturer")
            or getattr(self.instance, "manufacturer", None)
        )

        if manufacturer:
            self.fields["license"].queryset = License.objects.filter(manufacturer=manufacturer)

        if self.instance.pk:
            self.fields["manufacturer"].disabled = True
            self.fields["license"].disabled = True
            self.fields["device"].disabled = True
            self.fields["virtual_machine"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        device = cleaned_data.get("device")
        virtual_machine = cleaned_data.get("virtual_machine")
        license_obj = cleaned_data.get("license")

        if not device and not virtual_machine:
            raise forms.ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if device and virtual_machine:
            raise forms.ValidationError("You can only assign a license to either a Device or a Virtual Machine, not both.")

        if license_obj:
            license_obj.is_child_license = bool(license_obj.parent_license)
            license_obj.is_parent_license = license_obj.sub_licenses.exists()

        return cleaned_data

    def save(self, commit=True):
        assignment = super().save(commit=False)

        if self.cleaned_data.get("virtual_machine"):
            assignment.virtual_machine = self.cleaned_data["virtual_machine"]
            assignment.device = None
        elif self.cleaned_data.get("device"):
            assignment.device = self.cleaned_data["device"]
            assignment.virtual_machine = None

        if commit:
            assignment.save()

        return assignment
    
class LicenseTypeFilterForm(NetBoxModelFilterSetForm):
    model = LicenseType
    filterset_class = filtersets.LicenseTypeFilterSet

    fieldsets = (
        FieldSet('q', name='Search'),
        FieldSet('manufacturer_id', 'volume_type', 'license_model', 'purchase_model', name='Details'),
    )

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer"
    )

    volume_type = forms.ChoiceField(
        choices=[('', '---------')] + LicenseType.VOLUME_TYPE_CHOICES,
        required=False,
        label="Volume Type"
    )

    license_model = forms.ChoiceField(
        choices=[('', '---------')] + LicenseType.LICENSE_MODEL_CHOICES,
        required=False,
        label="License Model"
    )

    purchase_model = forms.ChoiceField(
        choices=[('', '---------')] + LicenseType.PURCHASE_MODEL_CHOICES,
        required=False,
        label="Purchase Model"
    )

    q = forms.CharField(
        required=False,
        label='Search'
    )


class LicenseTypeImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license type manufacturer'
    )

    class Meta:
        model = LicenseType
        fields = [
            "name", "slug", "manufacturer", "product_code", "ean_code",
            "volume_type", "license_model", "purchase_model", "description"
        ]
        labels = {
            "name": "Name",
            "slug": "Slug",
            "manufacturer": "Manufacturer",
            "product_code": "Product Code",
            "ean_code": "EAN Code",
            "volume_type": "Volume Type",
            "license_model": "License Model",
            "purchase_model": "Purchase Model",
            "description": "Description",
        }
        help_texts = {
            "name": "Name of the license type",
            "slug": "URL-friendly identifier",
            "manufacturer": "Manufacturer of the license type",
            "product_code": "Internal or external product code",
            "ean_code": "European Article Number",
            "volume_type": "Type of volume: single, volume, or unlimited",
            "license_model": "Base license or expansion pack",
            "purchase_model": "Peripheral or subscription",
            "description": "Optional notes",
        }

class LicenseTypeBulkEditForm(forms.ModelForm):
    class Meta:
        model = LicenseType
        fields = [
            "name",
            "slug",
            "manufacturer",
            "product_code",
            "ean_code",
            "volume_type",
            "license_model",
            "purchase_model",
            "description",
            "comments",
        ]

class LicenseAssignmentImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer'
    )

    license = CSVModelChoiceField(
        queryset=License.objects.all(),
        to_field_name='license_key',
        label='License',
        help_text='Assigned license (by license key)'
    )

    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name='name',
        required=False,
        label='Device',
        help_text='Device to assign the license to (optional)'
    )

    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        required=False,
        label='Virtual Machine',
        help_text='Virtual machine to assign the license to (optional)'
    )

    class Meta:
        model = LicenseAssignment
        fields = ["manufacturer", "license", "device", "virtual_machine", "volume", "description"]
        labels = {
            "manufacturer": "Manufacturer",
            "license": "License",
            "device": "Device",
            "virtual_machine": "Virtual Machine",
            "volume": "Volume",
            "description": "Description",
        }
        help_texts = {
            "manufacturer": "The license manufacturer",
            "license": "License assigned by license key",
            "device": "Device name (if applicable)",
            "virtual_machine": "VM name (if applicable)",
            "volume": "How many units are assigned",
            "description": "Optional description of the assignment",
        }

    def clean(self):
        super().clean()
        device = self.cleaned_data.get("device")
        virtual_machine = self.cleaned_data.get("virtual_machine")

        if not device and not virtual_machine:
            raise forms.ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if device and virtual_machine:
            raise forms.ValidationError("A license can only be assigned to a Device or a Virtual Machine, not both.")


class LicenseAssignmentBulkEditForm(forms.ModelForm):
    class Meta:
        model = LicenseAssignment
        fields = ["license", "device", "volume", "description"]


class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    filterset_class = LicenseAssignmentFilterSet

    manufacturer_id = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer",
    )

    device_manufacturer_id = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Device Manufacturer"
    )

    virtual_machine__cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label="Cluster"
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="License",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device"
    )

    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine"
    )

    comments = CommentField()

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer_id", "device_manufacturer_id", "cluster_id",
            "device_id", "virtual_machine_id", "license", "assigned_to", "volume", "comments"
        ]
