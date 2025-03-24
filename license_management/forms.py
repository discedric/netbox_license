from django import forms
from .models import License, LicenseAssignment
from dcim.models import Manufacturer, Device
from utilities.forms.fields import DynamicModelChoiceField
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
        label="Manufacturer",
        selector=True
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        selector=True
    )

class LicenseImportForm(forms.ModelForm):
    """Form for importing Licenses in bulk."""

    class Meta:
        model = License
        fields = [
            "license_key",
            "product_key",
            "serial_number",
            "name",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "volume_type",
            "volume_limit",
            "parent_license",
        ]


class LicenseBulkEditForm(forms.ModelForm):
    """Form for bulk editing Licenses."""

    class Meta:
        model = License
        fields = [
            "name",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "volume_type",
            "volume_limit",
            "parent_license",
        ]

    

class LicenseForm(forms.ModelForm):
    """Form for adding/editing a software license"""

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="Manufacturer",
        selector=True, 
        quick_add=True  
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        help_text="Select a parent license if applicable.",
        selector=True,
        query_params={  
            'manufacturer_id': '$manufacturer',  
        }
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

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Comment"
    )

    class Meta:
        model = License
        fields = [
            "manufacturer",
            "name",
            "license_key",
            "product_key",
            "serial_number",
            "description",
            "volume_type",
            "volume_limit",
            "parent_license",
            "purchase_date",
            "expiry_date",
            "comment"  
        ]

    def clean(self):
        cleaned_data = super().clean()
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
        label="Manufacturer",
        selector=True,
        quick_add=True
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.none(),  # Will be set in __init__
        required=True,
        label="License",
        selector=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    device_manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Device Manufacturer",
        selector=True,
        help_text="Select a manufacturer to filter Devices (optional)"
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.none(),  # Will be set in __init__
        required=False,
        label="Device",
        selector=True,
        query_params={"manufacturer_id": "$device_manufacturer"}
    )

    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label="Cluster",
        selector=True,
        help_text="Select a cluster to filter Virtual Machines (optional)"
    )

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine",
        query_params={'cluster_id': '$cluster'}
    )

    fieldsets = (
        FieldSet(
            "manufacturer", "license", "volume", "description",
            name="General Information"
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("device_manufacturer", "device", name="Device Assignment"),
                FieldSet("cluster", "virtual_machine", name="Virtual Machine Assignment"),
            ),
            name="Assignment Type"
        ),
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer", "license",
            "device_manufacturer", "device",
            "cluster", "virtual_machine",
            "volume", "description"
        ]
        error_messages = {
            "device": {"required": "You must select a device or virtual machine."},
            "virtual_machine": {"required": "You must select a device or virtual machine."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        license_manufacturer_id = self._get_value("manufacturer")
        if license_manufacturer_id:
            self.fields["license"].queryset = License.objects.filter(manufacturer_id=license_manufacturer_id)

        device_manufacturer_id = self._get_device_manufacturer_id()
        if device_manufacturer_id:
            self.fields["device"].queryset = Device.objects.filter(device_type__manufacturer_id=device_manufacturer_id)
            self.fields["device"].widget.add_query_param("device_type__manufacturer_id", device_manufacturer_id)
        else:
            self.fields["device"].queryset = Device.objects.none()

    def _get_value(self, field_name):
        """Helper to get a field value from data, initial, or instance"""
        if self.data.get(field_name):
            return self.data.get(field_name)
        if self.initial.get(field_name):
            return self.initial.get(field_name)
        if self.instance and getattr(self.instance, field_name, None):
            return getattr(self.instance, field_name).pk
        return None

    def _get_device_manufacturer_id(self):
        """Special case for resolving device manufacturer"""
        if self.data.get("device_manufacturer"):
            return self.data.get("device_manufacturer")
        if self.initial.get("device_manufacturer"):
            return self.initial["device_manufacturer"]
        if self.instance and self.instance.device:
            return self.instance.device.device_type.manufacturer_id
        return None

    def clean(self):
        cleaned_data = super().clean()
        if not isinstance(cleaned_data, dict):
            cleaned_data = self.cleaned_data


        device = cleaned_data.get("device")
        virtual_machine = cleaned_data.get("virtual_machine")

        if not device and not virtual_machine:
            raise forms.ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if device and virtual_machine:
            raise forms.ValidationError("You can only assign a license to either a Device or a Virtual Machine, not both.")

        return cleaned_data



class LicenseAssignmentImportForm(forms.ModelForm):
    """Form for bulk importing License Assignments."""

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer",
            "license",
            "device",
            "volume",
            "description",
        ]


class LicenseAssignmentBulkEditForm(forms.ModelForm):
    """Form for bulk editing License Assignments."""

    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "volume",
            "description",
        ]

class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    """Filter form for License Assignments with advanced searching."""
    
    model = LicenseAssignment 

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer",
        selector=True
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device",
        selector=True
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="License",
        selector=True
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        selector=True
    )

    class Meta:
        model = LicenseAssignment  
        fields = [
            "license",
            "device",
            "manufacturer",
            "assigned_to",
            "volume",
            "parent_license",
        ]

    filterset_class = LicenseAssignmentFilterSet 