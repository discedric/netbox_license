from django import forms
from .models import License, LicenseAssignment
from dcim.models import Manufacturer, Device
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from .filtersets import LicenseAssignmentFilterSet, LicenseFilterSet
from virtualization.models import VirtualMachine, Cluster
from utilities.forms.rendering import FieldSet, TabbedGroups

class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    filterset_class = LicenseFilterSet

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer", 
        selector=True
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        selector=True
    )

    


class LicenseImportForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "license_key", "product_key", "serial_number", "name", "description",
            "manufacturer", "purchase_date", "expiry_date",
            "volume_type", "volume_limit", "parent_license",
        ]


class LicenseBulkEditForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "name", "description", "manufacturer", "purchase_date",
            "expiry_date", "volume_type", "volume_limit", "parent_license",
        ]


class LicenseForm(NetBoxModelForm):

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
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

    name = forms.CharField(
        required=True,
        label="Name"
    )

    volume_type = forms.ChoiceField(
        choices=License.VOLUME_TYPE_CHOICES,
        required=True,
        label="Volume Type"
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
            "manufacturer", "name", "license_key", "product_key", "serial_number", "description",
            "volume_type", "volume_limit", "parent_license", "purchase_date", "expiry_date", "comment"
        ]

        def clean(self):
            cleaned_data = super().clean()

            if not cleaned_data:
                return cleaned_data

            volume_type = cleaned_data.get("volume_type")
            volume_limit = cleaned_data.get("volume_limit")

            if volume_type == "SINGLE":
                cleaned_data["volume_limit"] = 1
            elif volume_type == "UNLIMITED":
                cleaned_data["volume_limit"] = None
            elif volume_type == "VOLUME":
                if volume_limit is None or volume_limit < 2:
                    self.add_error("volume_limit", "Volume licenses require a volume limit of at least 2.")

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

    device_manufacturer_display = forms.CharField(
        required=False,
        label="Device Manufacturer",
        disabled=True
    )

    cluster_display = forms.CharField(
        required=False,
        label="Cluster",
        disabled=True
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            "manufacturer", "license", "volume", "description",
            name="General Information"
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("device", "device_manufacturer_display", name="Device Assignment"),
                FieldSet("virtual_machine", "cluster_display", name="Virtual Machine Assignment"),
            ),
            name="Assignment Type"
        ),
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer", "license", "device", "virtual_machine",
            "volume", "description",'comments'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        manufacturer = self.data.get("manufacturer") or self.initial.get("manufacturer") or getattr(self.instance, "manufacturer", None)

        if manufacturer:
            self.fields["license"].queryset = License.objects.filter(manufacturer=manufacturer)

        if self.instance.pk:
            self.fields['manufacturer'].disabled = True
            self.fields['license'].disabled = True
            self.fields['device'].disabled = True
            self.fields['virtual_machine'].disabled = True

            if self.instance.device:
                self.fields['device_manufacturer_display'].initial = self.instance.device.device_type.manufacturer.name
            elif self.instance.virtual_machine:
                self.fields['cluster_display'].initial = self.instance.virtual_machine.cluster.name

        else:
            if self.data.get("device"):
                self.fields['virtual_machine'].disabled = True
                self.fields['cluster_display'].initial = "(disabled)"
            elif self.data.get("virtual_machine"):
                self.fields['device'].disabled = True
                self.fields['device_manufacturer_display'].initial = "(disabled)"

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        device = cleaned_data.get("device")
        virtual_machine = cleaned_data.get("virtual_machine")

        device = cleaned_data.get("device")
        virtual_machine = cleaned_data.get("virtual_machine")

        if not device and not virtual_machine:
            raise forms.ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if device and virtual_machine:
            raise forms.ValidationError("You can only assign a license to either a Device or a Virtual Machine, not both.")

        if device:
            cleaned_data['device_manufacturer_display'] = device.device_type.manufacturer.name
        if virtual_machine:
            cleaned_data['cluster_display'] = virtual_machine.cluster.name

        return cleaned_data

    def save(self, commit=True):
        assignment = super().save(commit=False)

        if self.cleaned_data.get('virtual_machine'):
            assignment.virtual_machine = self.cleaned_data['virtual_machine']
            assignment.device = None
        elif self.cleaned_data.get('device'):
            assignment.device = self.cleaned_data['device']
            assignment.virtual_machine = None

        if commit:
            assignment.save()

        return assignment

class LicenseAssignmentImportForm(forms.ModelForm):
    class Meta:
        model = LicenseAssignment
        fields = ["manufacturer", "license", "device", "volume", "description"]


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
        selector=True
    )
    device_manufacturer_id = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Device Manufacturer",
        selector=True,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device",
        selector=True,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="License",
        selector=True,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )

    comments = CommentField()

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer", "device_manufacturer",
            "device", "license", "assigned_to", "volume",
            'comments'
        ]
