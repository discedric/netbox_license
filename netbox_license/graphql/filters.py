import strawberry_django
from netbox.graphql.filters_mixins import autotype_decorator, BaseFilterMixin
from netbox_license import models
from netbox_license.filtersets import licenseassignments
from netbox_license.filtersets.licenses import LicenseFilterSet

__all__= (
    'LicenseFilter',
    'LicenseAssignmentFilter',
)

@strawberry_django.filter(models.License, lookups=True)
@autotype_decorator(LicenseFilterSet)
class LicenseFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.LicenseAssignment, lookups=True)
@autotype_decorator(licenseassignments.LicenseAssignmentFilterSet)
class LicenseAssignmentFilter(BaseFilterMixin):
    pass