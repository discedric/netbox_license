import django_filters
from .models import License, LicenseAssignment
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer, Device

class LicenseFilterSet(NetBoxModelFilterSet):
    """Filterset for Software Licenses with enhanced search capability."""

    q = django_filters.CharFilter(method="search", label="Search")
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(), label="Manufacturer"
    )
    assignment_type = django_filters.ChoiceFilter(
        choices=License.ASSIGNMENT_TYPE_CHOICES,
        label="Assignment Type"
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
            "assignment_type",
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
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device"
    )
    assigned_to = django_filters.DateFromToRangeFilter(
        label="Assigned Date (Between)"
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "assigned_to",
            "volume",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            license__software_name__icontains=value
        ) | queryset.filter(
            device__name__icontains=value
        ) | queryset.filter(
            license__license_key__icontains=value
        )
