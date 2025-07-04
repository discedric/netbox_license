from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType
from dcim.graphql.types import ManufacturerType, DeviceType
from virtualization.graphql.types import VirtualMachineType


from netbox_license.models import LicenseType, License, LicenseAssignment


### Basic GraphQL setup without filtering options


# ───── OBJECT TYPES  ──────────────────────────────────────────────

@strawberry_django.type(
    LicenseType,
    fields='__all__',
)
class LicenseTypeType(NetBoxObjectType):
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]



@strawberry_django.type(
    License,
    fields='__all__',
)
class LicenseType(NetBoxObjectType):
    license_type: Annotated["LicenseTypeType", strawberry.lazy('netbox_license.graphql')]



@strawberry_django.type(
    LicenseAssignment,
    fields='__all__',
)
class LicenseAssignmentType(NetBoxObjectType):
    license: Annotated["LicenseType", strawberry.lazy("netbox_license.graphql")]
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")] | None
    virtual_machine: Annotated["VirtualMachineType", strawberry.lazy("virtualization.graphql.types")] | None




# ───── QUERY CLASS  ─────────────────────────────────────────────────

@strawberry.type
class LicenseTypeQuery:
    @strawberry.field
    def license_type(self, id: int) -> LicenseTypeType:
        return None
    license_type_list: List[LicenseTypeType] = strawberry_django.field()



@strawberry.type
class LicenseQuery:
    @strawberry.field
    def license(self, id: int) -> LicenseType:
        return None
    license_list: List[LicenseType] = strawberry_django.field()



@strawberry.type
class LicenseAssignmentQuery:
    @strawberry.field
    def license_assignment(self, id: int) -> LicenseAssignmentType:
        return None
    license_assignment_list: List[LicenseAssignmentType] = strawberry_django.field()




# ───── SCHEMA  ─────────────────────────────────────────────────

schema = [
    LicenseTypeQuery,
    LicenseQuery,
    LicenseAssignmentQuery,
]