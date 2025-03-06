import django_filters
from .models import License, LicenseAssignment
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer

class LicenseFilterSet(NetBoxModelFilterSet):
    """Filterset for Software Licenses"""
    q = django_filters.CharFilter(method="search", label="Search")
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(), label="Manufacturer"
    )  

    class Meta:
        model = License
        fields = [
            "license_key",
            "software_name",
            "manufacturer",
            "type",
            "status",
            "assignment_type",
            "purchase_date",
            "expiry_date",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            software_name__icontains=value
        ) | queryset.filter(
            license_key__icontains=value
        )


class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    """Filterset for License Assignments"""
    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "status",
            "assigned_on", 
        ]
