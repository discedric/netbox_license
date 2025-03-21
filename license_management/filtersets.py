import django_filters
from django.db.models import Q
from .models import License, LicenseAssignment
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer, Device

class LicenseFilterSet(NetBoxModelFilterSet):
    """Filterset for Software Licenses with enhanced search capability."""

    q = django_filters.CharFilter(method="search", label="Search")
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(), label="Manufacturer"
    )
    volume_type = django_filters.ChoiceFilter(
        choices=License.VOLUME_TYPE_CHOICES,
        label="Volume Type"
    )
    purchase_date = django_filters.DateFromToRangeFilter(label="Purchase Date (Between)")
    expiry_date = django_filters.DateFromToRangeFilter(label="Expiry Date (Between)")
    parent_license = django_filters.ModelChoiceFilter(
        queryset=License.objects.all(),
        label="Parent License"
    )

    class Meta:
        model = License
        fields = [
            "license_key",
            "product_key",
            "serial_number",
            "name",
            "manufacturer",
            "volume_type",
            "purchase_date",
            "expiry_date",
            "parent_license",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            name__icontains=value
        ) | queryset.filter(
            license_key__icontains=value
        ) | queryset.filter(
            product_key__icontains=value
        ) | queryset.filter(
            serial_number__icontains=value
        )


class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    """Filterset for License Assignments with added filtering fields."""

    q = django_filters.CharFilter(method="search", label="Search")

    license = django_filters.ModelChoiceFilter(
        queryset=License.objects.all(),
        label="License"
    )
    parent_license = django_filters.ModelChoiceFilter(
        queryset=License.objects.filter(parent_license__isnull=False),
        method="filter_parent_license",
        label="Parent License"
    )
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device"
    )
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(),
        field_name="license__manufacturer",
        label="Manufacturer"
    )
    assigned_to = django_filters.DateFromToRangeFilter(
        label="Assigned Date (Between)"
    )
    volume = django_filters.NumberFilter(
        field_name="volume",
        label="Volume"
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "manufacturer",
            "assigned_to",
            "volume",
        ]

    def search(self, queryset, name, value):
        """Search in license name, license key, manufacturer name, and device name."""
        return queryset.filter(
            Q(license__name__icontains=value) |
            Q(license__license_key__icontains=value) |
            Q(license__manufacturer__name__icontains=value) |
            Q(device__name__icontains=value)
        )

    def filter_parent_license(self, queryset, name, value):
        """Filter the assignments to only include the selected parent license and its children."""
        if value:
            return queryset.filter(
                Q(license=value) |
                Q(license__parent_license=value)
            )
        return queryset

