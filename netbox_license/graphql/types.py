from typing import Annotated, Optional

import strawberry
import strawberry_django

from django.utils import timezone

from netbox.graphql.types import NetBoxObjectType
from netbox_license.models.license import License
from netbox_license.models.licenseassignment import LicenseAssignment
from netbox_license.models.licensetype import LicenseType

from .filters import (
    LicenseFilter,
    LicenseAssignmentFilter,
    LicenseTypeFilter,
)

@strawberry_django.type(LicenseType, fields='__all__', filters=LicenseTypeFilter)
class LicenseTypeType(NetBoxObjectType):
    pass


@strawberry_django.type(License, fields='__all__', filters=LicenseFilter)
class LicenseObjectType(NetBoxObjectType):
    manufacturer: Annotated["ManufacturerType", strawberry.lazy("dcim.graphql.types")]

    @strawberry.field
    def is_expired(self) -> bool:
        return bool(self.expiry_date and self.expiry_date < timezone.now().date())

    @strawberry.field
    def days_until_expiry(self) -> Optional[int]:
        if self.expiry_date:
            delta = self.expiry_date - timezone.now().date()
            return max(delta.days, 0)
        return None



@strawberry_django.type(LicenseAssignment, fields='__all__', filters=LicenseAssignmentFilter)
class LicenseAssignmentType(NetBoxObjectType):
    license: Annotated["LicenseObjectType", strawberry.lazy("netbox_license.graphql.types")]
    manufacturer: Annotated["ManufacturerType", strawberry.lazy("dcim.graphql.types")]
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")] | None
    virtual_machine: Annotated["VirtualMachineType", strawberry.lazy("virtualization.graphql.types")] | None

    @strawberry.field
    def device_type(self) -> Optional[Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")]]:
        if self.device:
            return self.device.device_type
        return None
