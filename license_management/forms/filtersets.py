from django import forms
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine, Cluster
from license_management.models import License, LicenseType, LicenseAssignment, LicenseModel
from license_management import filtersets


class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    filterset_class = filtersets.LicenseFilterSet

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

    license_model = DynamicModelMultipleChoiceField(
        queryset=LicenseModel.objects.all(),
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


class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    filterset_class = filtersets.LicenseAssignmentFilterSet

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
            "manufacturer_id",
            "device_manufacturer_id",
            "virtual_machine__cluster_id",
            "device_id",
            "virtual_machine_id",
            "license",
            "assigned_to",
            "volume",
            "comments"
        ]
