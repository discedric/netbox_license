from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.scalars import BigInt
from netbox.graphql.types import (
    NetBoxObjectType,
    OrganizationalObjectType,
)
from license_management.models import (
   License,
   LicenseAssignment,
)
from .filters import (
    LicenseFilter,
    LicenseAssignmentFilter,
)

@strawberry_django.type(License, fields='__all__', filters=LicenseFilter)
class LicenseType(NetBoxObjectType):
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]
    device_type: Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")] | None

@strawberry_django.type(LicenseAssignment, fields='__all__', filters=LicenseAssignmentFilter)
class LicenseAssignmentType(NetBoxObjectType):
    license: Annotated["LicenseType", strawberry.lazy("license_management.graphql.types")]
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]
    device_type: Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")] | None
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')] | None
    