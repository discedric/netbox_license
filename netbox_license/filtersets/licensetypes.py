import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q
from netbox_license.models.licensetype import LicenseType

from netbox_license.choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
)
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer

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

    license_model = django_filters.MultipleChoiceFilter(
        choices=LicenseModelChoices,
        label="License Model"
    )


    base_license = django_filters.ModelMultipleChoiceFilter(
        queryset=LicenseType.objects.filter(license_model="base"),
        label="Base License"
    )

    name = django_filters.CharFilter(lookup_expr='icontains', label="Name")
    slug = django_filters.CharFilter(lookup_expr='icontains', label="Slug")
    product_code = django_filters.CharFilter(lookup_expr='icontains', label="Product Code")
    ean_code = django_filters.CharFilter(lookup_expr='icontains', label="EAN Code")
    volume_type = django_filters.ChoiceFilter(choices=VolumeTypeChoices, label="Volume Type")
    purchase_model = django_filters.ChoiceFilter(choices=PurchaseModelChoices, label="Purchase Model")

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
