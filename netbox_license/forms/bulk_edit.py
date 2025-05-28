from django import forms
from netbox_license.models.license import License
from netbox_license.models.licenseassignment import LicenseAssignment
from netbox_license.models.licensetype import LicenseType
from dcim.models import Device, Manufacturer
from utilities.forms.widgets import DatePicker
from virtualization.models import VirtualMachine
from ..choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
    VolumeRelationChoices,
    LicenseStatusChoices,
    LicenseAssignmentStatusChoices
)
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField


# ---------- LicenseType ----------

class LicenseTypeBulkEditForm(NetBoxModelBulkEditForm):
    model = LicenseType

    name = forms.CharField(
        required=False,
        label="Name"
    )

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer",
        selector=True
    )

    product_code = forms.CharField(
        required=False,
        label="Product Code"
    )

    ean_code = forms.CharField(
        required=False,
        label="EAN Code"
    )

    volume_type = forms.ChoiceField(
        choices=[('', '---------')] + list(VolumeTypeChoices),
        required=False,
        label="Volume Type"
    )

    volume_relation = forms.ChoiceField(
        choices=[('', '---------')] + list(VolumeRelationChoices),
        required=False,
        label="Volume Relation"
    )

    license_model = forms.ChoiceField(
        choices=[('', '---------')] + list(LicenseModelChoices),
        required=False,
        label="License Model"
    )

    base_license = DynamicModelChoiceField(
        queryset=LicenseType.objects.filter(license_model=LicenseModelChoices.BASE),
        required=False,
        label="Base License",
        selector=True,
        query_params={
            "license_model": LicenseModelChoices.BASE,
            "manufacturer_id": "$manufacturer",
        }
    )

    purchase_model = forms.ChoiceField(
        choices=[('', '---------')] + list(PurchaseModelChoices),
        required=False,
        label="Purchase Model"
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput,
        label="Description"
    )

    comment = CommentField()

    class Meta:
        fields = (
            "name", "manufacturer", "product_code", "ean_code",
            "volume_type", "volume_relation", "license_model", "base_license",
            "purchase_model", "description", "comment", "tags"
        )


# ---------- License ----------

class LicenseBulkEditForm(NetBoxModelBulkEditForm):
    model = License

    license_type = DynamicModelChoiceField(
        queryset=LicenseType.objects.all(),
        required=False,
        label="License Type",
        selector=True,
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        selector=True,
        query_params={"license_type__manufacturer_id": "$license_type__manufacturer"}
    )

    purchase_date = forms.DateField(
        required=False,
        widget=DatePicker(attrs={'is_clearable': True}),
        label="Purchase Date"
    )

    expiry_date = forms.DateField(
        required=False,
        widget=DatePicker(attrs={'is_clearable': True}),
        label="Expiry Date"
    )

    volume_limit = forms.IntegerField(
        required=False,
        label="Volume Limit"
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput,
        label="Description"
    )

    comment = CommentField()

    class Meta:
        fields = [
            "license_type", "description", "volume_limit",
            "parent_license", "purchase_date", "expiry_date", "comment"
        ]
# ---------- Assignments ----------

class LicenseAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    model = LicenseAssignment

    license_type = DynamicModelChoiceField(
        queryset=LicenseType.objects.all(),
        required=False,
        label="License Type",
        selector=True,
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.none(),
        required=False,
        label="License",
        selector=True,
        query_params={"license__license_type__manufacturer_id": "$license_type__manufacturer"}
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

    volume = forms.IntegerField(
        required=False,
        label="Volume"
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput,
        label="Description"
    )

    comment = CommentField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        license_type = self.initial.get("license_type") or self.data.get("license_type")
        if license_type:
            self.fields["license"].queryset = License.objects.filter(license_type=license_type)

    class Meta:
        fields = [
            "license_type", "license", "device", "virtual_machine",
            "volume", "description", "comment"
        ]
