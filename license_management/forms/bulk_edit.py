from django import forms
from license_management.models import License, LicenseType, LicenseAssignment
from dcim.models import Device, Manufacturer
from virtualization.models import VirtualMachine, Cluster
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField, SlugField


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
        choices=[('', '---------')] + LicenseType.VOLUME_TYPE_CHOICES,
        required=False,
        label="Volume Type"
    )

    license_model = forms.ChoiceField(
        choices=LicenseType.LICENSE_MODEL_CHOICES,
        required=False,
        label="License Model"
    )

    base_license = DynamicModelChoiceField(
        queryset=LicenseType.objects.filter(license_model="BASE"),
        required=False,
        label="Base License",
        selector=True,
        query_params={
            "license_model": "BASE",
            "manufacturer_id": "$manufacturer",
        }
    )

    purchase_model = forms.ChoiceField(
        choices=[('', '---------')] + LicenseType.PURCHASE_MODEL_CHOICES,
        required=False,
        label="Purchase Model"
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput,
        label="Description"
    )

    comments = CommentField()

    class Meta:
        fields = (
            "name", "manufacturer", "product_code", "ean_code",
            "volume_type", "license_model", "base_license",
            "purchase_model", "description", "comments", "tags"
        )

# ---------- License ----------

class LicenseBulkEditForm(NetBoxModelBulkEditForm):
    model = License

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer",
        selector=True
    )

    license_type = DynamicModelChoiceField(
        queryset=LicenseType.objects.all(),
        required=False,
        label="License Type",
        selector=True,
        query_params={"manufacturer_id": "$manufacturer"}
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        selector=True,
        query_params={"manufacturer_id": "$manufacturer"}
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
            "manufacturer", "license_type", "description", "volume_limit",
            "parent_license", "purchase_date", "expiry_date", "comment"
        ]

# ---------- Assignments ----------

class LicenseAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    model = LicenseAssignment

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer",
        selector=True
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.none(),
        required=False,
        label="License",
        selector=True,
        query_params={"manufacturer_id": "$manufacturer"}
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

    comments = CommentField()

    class Meta:
        fields = [
            "manufacturer", "license", "device", "virtual_machine",
            "volume", "description", "comments"
        ]
