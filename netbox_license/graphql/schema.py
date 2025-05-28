import strawberry
import strawberry_django

from netbox_license.models.license import License
from netbox_license.models.licenseassignment import LicenseAssignment
from netbox_license.models.licensetype import LicenseType
from .types import LicenseType, LicenseAssignmentType


@strawberry_django.type
class LicenseQuery:
    @strawberry_django.field
    def license(self, info, id: int) -> LicenseType:
        return License.objects.get(pk=id)

    license_list: list[LicenseType] = strawberry_django.field()


@strawberry_django.type
class LicenseAssignmentQuery:
    @strawberry_django.field
    def license_assignment(self, info, id: int) -> LicenseAssignmentType:
        return LicenseAssignment.objects.get(pk=id)

    license_assignment_list: list[LicenseAssignmentType] = strawberry_django.field()
