from django import forms
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine, Cluster
from license_management.models import License, LicenseType, LicenseAssignment
from license_management import filtersets
from ..choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
    VolumeRelationChoices,
    LicenseStatusChoices,
    LicenseAssignmentStatusChoices
)

# ---------- LicenseType ----------

class LicenseTypeFilterForm(NetBoxModelFilterSetForm):
    model = LicenseType
    filterset_class = filtersets.LicenseTypeFilterSet

    fieldsets = (
        FieldSet('q', name='Search'),
        FieldSet(
            'manufacturer_id',
            'volume_type',
            'license_model',
            'purchase_model',
            'base_license',
            name='Details'
        ),
    )
    

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer"
    )

    volume_type = forms.ChoiceField(
        choices=VolumeTypeChoices,
        required=False,
        label="Volume Type"
    )

    license_model = forms.ChoiceField(
        choices=LicenseModelChoices,
        required=False,
        label="License Model"
    )

    purchase_model = forms.ChoiceField(
        choices=PurchaseModelChoices,
        required=False,
        label="Purchase Model"
    )

    base_license = DynamicModelMultipleChoiceField(
        queryset=LicenseType.objects.filter(license_model="base"),
        required=False,
        label="Base License",
        query_params={
            "license_model": "BASE",
        }
    )

    q = forms.CharField(
        required=False,
        label='Search'
    )

# ---------- License ----------

class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    filterset_class = filtersets.LicenseFilterSet

    selector_fields = (
        'manufacturer_id',
        'volume_type',
        'license_model',
        'license_type_id',
    )

    fieldsets = (
        FieldSet('q', name='Search'),
        FieldSet('manufacturer_id', 'license_key', name='License Info'),
        FieldSet('license_model', 'volume_type', 'license_type_id', name='License Type Info'),
        FieldSet('is_parent_license', 'is_child_license', 'parent_license', 'child_license', name='License Relationship'),
        FieldSet('purchase_date_after', 'purchase_date_before', 'expiry_date_after', 'expiry_date_before', name='Dates'),
    )

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer"
    )

    volume_type = forms.MultipleChoiceField(
        required=False,
        label="Volume Type",
        choices= VolumeTypeChoices,
        widget=forms.SelectMultiple()
    )

    license_model = forms.MultipleChoiceField(
        required=False,
        label="License Model",
        choices= LicenseModelChoices,
        widget=forms.SelectMultiple()
    )

    license_type_id = DynamicModelMultipleChoiceField(
        required=False,
        label="License Type",
        queryset=LicenseType.objects.all(),
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    parent_license = DynamicModelMultipleChoiceField(
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

# ---------- Assignments ----------

class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    filterset_class = filtersets.LicenseAssignmentFilterSet

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer",
    )

    device_manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Device Manufacturer"
    )

    virtual_machine__cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label="Cluster"
    )

    license = DynamicModelMultipleChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="License",
        query_params={'manufacturer_id': '$manufacturer_id'},
        display_field="license_key",
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

    fieldsets = (
        FieldSet('manufacturer_id', 'license', name='License Info'),
        FieldSet('device_manufacturer_id', 'device_id', 'virtual_machine_id', 'virtual_machine__cluster_id', name='Assignment Target'),
        FieldSet('volume', 'comments', name='Metadata'),
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer_id",
            "device_manufacturer_id",
            "device_id",
            "virtual_machine__cluster_id",
            "virtual_machine_id",
            "license",
            "assigned_to",
            "volume",
            "comments"
        ]