import strawberry_django
from netbox.graphql.filters_mixins import BaseFilterMixin
from netbox_license import models


__all__= (
    'LicenseTypeFilter',
    'LicenseFilter',
    'LicenseAssignmentFilter',
)

@strawberry_django.filter(models.LicenseType, lookups=True)
class LicenseTypeFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.License, lookups=True)
class LicenseFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.LicenseAssignment, lookups=True)
class LicenseAssignmentFilter(BaseFilterMixin):
    pass