import strawberry_django
from netbox.graphql.filters_mixins import autotype_decorator, BaseFilterMixin
from license_management import filtersets, models

__all__= (
    'LicenseFilter',
    'LicenseAssignmentFilter',
)

@strawberry_django.filter(models.License, lookups=True)
@autotype_decorator(filtersets.LicenseFilterSet)
class LicenseFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.LicenseAssignment, lookups=True)
@autotype_decorator(filtersets.LicenseAssignmentFilterSet)
class LicenseAssignmentFilter(BaseFilterMixin):
    pass