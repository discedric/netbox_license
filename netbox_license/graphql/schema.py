import strawberry

from netbox_license.models.licensetype import LicenseType
from netbox_license.models.license import License
from netbox_license.models.licenseassignment import LicenseAssignment
from .types import (
    LicenseTypeType,
    LicenseObjectType,
    LicenseAssignmentType,
)

@strawberry.type
class LicenseTypeQuery:
    @strawberry.field
    def license_type(self, info, id: int) -> LicenseTypeType:
        return LicenseType.objects.get(pk=id)

    @strawberry.field
    def license_type_list(self, info) -> list[LicenseTypeType]:
        return list(LicenseType.objects.all())


@strawberry.type
class LicenseQuery:
    @strawberry.field
    def license(self, info, id: int) -> LicenseObjectType:
        return License.objects.get(pk=id)

    @strawberry.field
    def license_list(self, info) -> list[LicenseObjectType]:
        return list(License.objects.all())


@strawberry.type
class LicenseAssignmentQuery:
    @strawberry.field
    def license_assignment(self, info, id: int) -> LicenseAssignmentType:
        return LicenseAssignment.objects.get(pk=id)

    @strawberry.field
    def license_assignment_list(self, info) -> list[LicenseAssignmentType]:
        return list(LicenseAssignment.objects.all())
