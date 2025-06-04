import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q
from netbox_license.models.license import License
from netbox_license.models.licenseassignment import LicenseAssignment
from netbox_license.models.licensetype import LicenseType
from netbox_license.choices import AssignmentKindChoices
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer, Device, DeviceType
from virtualization.models import VirtualMachine, Cluster

class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    """Filterset for License Assignments with comprehensive filtering."""

    license = django_filters.ModelChoiceFilter(
        queryset=License.objects.all(),
        label="License"
    )
    license_id = django_filters.ModelMultipleChoiceFilter(
        field_name='license',
        queryset=License.objects.all(),
        label='License (ID)'
    )
    license__license_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name="license__license_type",
        queryset=LicenseType.objects.all(),
        label="License Type (ID)"
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name="license__license_type__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="License Manufacturer"
    )

    kind = django_filters.MultipleChoiceFilter(
        method='filter_kind',
        choices=AssignmentKindChoices,
        label="Kind",
    )

    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(), 
        label="Device"
    )
    
    virtual_machine = django_filters.ModelChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        label="Virtual Machine"
    )

    license__license_type__manufacturer_id = django_filters.ModelChoiceFilter(
        field_name="license__license_type__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="License Type Manufacturer"
    )
    device_manufacturer_id = django_filters.ModelChoiceFilter(
        field_name="device__device_type__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="Device Manufacturer"
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label="Device (ID)"
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device__device_type',
        queryset=DeviceType.objects.all(),
        label="Device Type"
    )

    virtual_machine_id = django_filters.ModelChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        label="Virtual Machine"
    )
    virtual_machine__cluster_id = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine__cluster',
        queryset=Cluster.objects.all(),
        label="Cluster"
    )

    assigned_to = django_filters.DateFromToRangeFilter(
        label="Assigned Date (Between)"
    )
    volume = django_filters.NumberFilter(
        label="Volume"
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "virtual_machine",
            "license__license_type__manufacturer",
            "device_manufacturer_id",
            "assigned_to",
            "volume",
            "kind",
        ]
   

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(license__license_key__icontains=value)
            | Q(license__serial_number__icontains=value)
            | Q(license__description__icontains=value)
            | Q(license__license_type__manufacturer__name__icontains=value)
            | Q(device__name__icontains=value)
            | Q(virtual_machine__name__icontains=value)
        ).distinct()
    
    def filter_kind(self, queryset, name, value):
        q = Q()
        if AssignmentKindChoices.DEVICE in value:
            q |= Q(device__isnull=False)
        if AssignmentKindChoices.VM in value:
            q |= Q(virtual_machine__isnull=False)
        return queryset.filter(q)

