from django import forms
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Manufacturer, Device, DeviceType
from virtualization.models import VirtualMachine, Cluster
from netbox_license.models import License, LicenseType, LicenseAssignment
from netbox_license import filtersets
from ..choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
    VolumeRelationChoices,
    LicenseStatusChoices,
    LicenseAssignmentStatusChoices,
    AssignmentKindChoices,
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
            'product_code',
            'ean_code',
            name='Details'
        ),
    )

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer"
    )

    volume_type = forms.MultipleChoiceField(
        choices=VolumeTypeChoices,
        required=False,
        label="Volume Type",
        widget=forms.SelectMultiple()
    )

    license_model = forms.MultipleChoiceField(
        choices=LicenseModelChoices,
        required=False,
        label="License Model",
        widget=forms.SelectMultiple()
    )

    purchase_model = forms.MultipleChoiceField(
        choices=PurchaseModelChoices,
        required=False,
        label="Purchase Model",
        widget=forms.SelectMultiple()
    )

    base_license = DynamicModelMultipleChoiceField(
        queryset=LicenseType.objects.filter(license_model="BASE"),
        required=False,
        label="Base License"
    )

    product_code = forms.CharField(required=False, label="Product Code")
    ean_code = forms.CharField(required=False, label="EAN Code")
    q = forms.CharField(required=False, label='Search')



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
        FieldSet('manufacturer_id', 'license_key', 'serial_number', 'name', name='License Info'),
        FieldSet('license_model', 'volume_type', 'license_type_id', name='License Type Info'),
        FieldSet('is_parent_license', 'is_child_license', 'parent_license', 'child_license', 'parent_license_type', name='License Relationship'),
        FieldSet('assignments__device_id', 'assignments__virtual_machine_id', 'assignments__virtual_machine__cluster_id', 'is_assigned', name='Assignment Info'),
        FieldSet('purchase_date', 'expiry_date', name='Dates'),
    )

    q = forms.CharField(required=False, label='Search')

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer"
    )

    license_key = forms.CharField(
        required=False,
        label="License Key"
    )

    serial_number = forms.CharField(
        required=False,
        label="Serial Number"
    )

    name = forms.CharField(
        required=False,
        label="Name"
    )

    license_model = forms.MultipleChoiceField(
        required=False,
        label="License Model",
        choices=LicenseModelChoices,
        widget=forms.SelectMultiple()
    )

    volume_type = forms.MultipleChoiceField(
        required=False,
        label="Volume Type",
        choices=VolumeTypeChoices,
        widget=forms.SelectMultiple()
    )

    license_type_id = DynamicModelMultipleChoiceField(
        queryset=LicenseType.objects.all(),
        required=False,
        label="License Type",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    parent_license = DynamicModelMultipleChoiceField(
        queryset=License.objects.filter(parent_license__isnull=True),
        required=False,
        label="Parent License",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    child_license = DynamicModelMultipleChoiceField(
        queryset=License.objects.exclude(parent_license__isnull=True),
        required=False,
        label="Child Licenses",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    parent_license_type = DynamicModelMultipleChoiceField(
        queryset=LicenseType.objects.all(),
        required=False,
        label="Parent License Type"
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

    is_assigned = forms.NullBooleanField(
        required=False,
        label="Is Assigned",
        widget=forms.Select(choices=[('', '---------'), (True, 'Yes'), (False, 'No')])
    )

    assignments__device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Assigned to Device"
    )

    assignments__virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Assigned to Virtual Machine"
    )

    assignments__virtual_machine__cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label="Assigned to Cluster"
    )

    purchase_date__gte = forms.DateField(
        required=False,
        label="Purchase Date (After)",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    purchase_date__lte = forms.DateField(
        required=False,
        label="Purchase Date (Before)",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    expiry_date__gte = forms.DateField(
        required=False,
        label="Expiry Date (After)",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    expiry_date__lte = forms.DateField(
        required=False,
        label="Expiry Date (Before)",
        widget=forms.DateInput(attrs={"type": "date"})
    )


# ---------- Assignments ----------

class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    filterset_class = filtersets.LicenseAssignmentFilterSet

    fieldsets = (
        FieldSet('q', name='Search'),
        FieldSet('manufacturer_id', 'license', 'license__license_type_id', name='License Info'),
        FieldSet('kind','device_manufacturer_id', 'device_id', 'device_type_id', 'virtual_machine_id', 'virtual_machine__cluster_id', name='Assignment Target'),
        FieldSet('assigned_to__gte', 'assigned_to__lte', 'volume', name='Assignment Details'),
        FieldSet('comments', name='Metadata'),
    )

    q = forms.CharField(required=False, label='Search')

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer",
    )

    license = DynamicModelMultipleChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="License",
        query_params={'manufacturer_id': '$manufacturer_id'},
    )

    license__license_type_id = DynamicModelMultipleChoiceField(
        queryset=LicenseType.objects.all(),
        required=False,
        label="License Type"
    )

    kind = forms.MultipleChoiceField(
        choices=AssignmentKindChoices,
        required=False,
        label="Kind",
        widget=forms.SelectMultiple()
    )

    device_manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Device Manufacturer"
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device"
    )

    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label="Device Type"
    )

    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine"
    )

    virtual_machine__cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label="Cluster"
    )

    assigned_to__gte = forms.DateField(
        required=False,
        label="Assigned Date (After)",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    assigned_to__lte = forms.DateField(
        required=False,
        label="Assigned Date (Before)",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    volume = forms.IntegerField(
        required=False,
        label="Volume"
    )

    comments = CommentField()
