import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q
from .models import License, LicenseAssignment, LicenseType
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine, Cluster

# ---------- LicenseType ----------

class LicenseTypeFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label="Manufacturer (ID)"
    )

    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label="Manufacturer name (slug)"
    )

    license_model = django_filters.ChoiceFilter(
        choices=LicenseType.LICENSE_MODEL_CHOICES,
        label="License Model"
    )

    base_license = django_filters.ModelMultipleChoiceFilter(
        queryset=LicenseType.objects.filter(license_model="BASE"),
        label="Base License"
    )

    name = django_filters.CharFilter(lookup_expr='icontains', label="Name")
    slug = django_filters.CharFilter(lookup_expr='icontains', label="Slug")
    product_code = django_filters.CharFilter(lookup_expr='icontains', label="Product Code")
    ean_code = django_filters.CharFilter(lookup_expr='icontains', label="EAN Code")
    volume_type = django_filters.ChoiceFilter(choices=LicenseType.VOLUME_TYPE_CHOICES, label="Volume Type")
    purchase_model = django_filters.ChoiceFilter(choices=LicenseType.PURCHASE_MODEL_CHOICES, label="Purchase Model")

    class Meta:
        model = LicenseType
        fields = [
            "name", "slug", "manufacturer", "product_code", "ean_code",
            "volume_type", "license_model", "purchase_model", "base_license"
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(product_code__icontains=value) |
            Q(ean_code__icontains=value)
        ).distinct()

# ---------- License ----------

class LicenseFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label=_('Manufacturer name (slug)'),
    )

    volume_type = django_filters.ChoiceFilter(
        choices=LicenseType.VOLUME_TYPE_CHOICES,
        label="Volume Type"
    )

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Name"
    )

    license_key = django_filters.CharFilter(
        lookup_expr='icontains',
        label="License Key"
    )

    serial_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Serial Number"
    )

    parent_license = django_filters.ModelChoiceFilter(
        queryset=License.objects.filter(parent_license__isnull=True),
        label="Parent License"
    )

    child_license = django_filters.ModelMultipleChoiceFilter(
        field_name='sub_licenses',
        queryset=License.objects.exclude(parent_license__isnull=True),
        label="Child Licenses"
    )

    is_parent_license = django_filters.BooleanFilter(
        method='filter_is_parent_license',
        label='Is Parent License'
    )

    is_child_license = django_filters.BooleanFilter(
        field_name='parent_license',
        lookup_expr='isnull',
        exclude=True,
        label='Is Child License'
    )
    

    purchase_date = django_filters.DateFromToRangeFilter(label="Purchase Date (Between)")
    expiry_date = django_filters.DateFromToRangeFilter(label="Expiry Date (Between)")

    class Meta:
        model = License
        fields = [
            "license_key", "serial_number", "name", "manufacturer", "volume_type",
            "purchase_date", "expiry_date", "parent_license", "child_license",
            "is_parent_license", "is_child_license",
        ]

    def filter_is_parent_license(self, queryset, name, value):
        if value:
            return queryset.filter(sub_licenses__isnull=False).distinct()
        return queryset.filter(sub_licenses__isnull=True)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(license_key__icontains=value) |
            Q(serial_number__icontains=value)
        ).distinct()

# ---------- Assignments ----------

class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    """Filterset for License Assignments with comprehensive filtering."""

    license = django_filters.ModelChoiceFilter(
        queryset=License.objects.all(),
        label="License"
    )

    device = django_filters.ModelChoiceFilter(queryset=Device.objects.all(), label="Device")
    
    virtual_machine = django_filters.ModelChoiceFilter(queryset=VirtualMachine.objects.all(), label="Virtual Machine")

    manufacturer_id = django_filters.ModelChoiceFilter(
        field_name="license__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="License Manufacturer"
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

    virtual_machine_id = django_filters.ModelChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        label="Virtual Machine"
    )

    virtual_machine__cluster_id = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine__cluster',
        queryset=Cluster.objects.all(),
        label="Cluster"
    )

    assigned_to = django_filters.DateFromToRangeFilter(label="Assigned Date (Between)")
    volume = django_filters.NumberFilter(label="Volume")

    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "virtual_machine",
            "manufacturer",
            "device_manufacturer",
            "assigned_to",
            "volume",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(license__name__icontains=value)
            | Q(license__license_key__icontains=value)
            | Q(license__manufacturer__name__icontains=value)
            | Q(device__name__icontains=value)
            | Q(virtual_machine__name__icontains=value)
        ).distinct()
