from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import LicenseSerializer, LicenseAssignmentSerializer, LicenseTypeSerializer
from netbox_license.filtersets.licenses import LicenseFilterSet
from netbox_license.filtersets import licenseassignments, licensetypes
from netbox_license.filtersets.licenses import LicenseFilterSet
from .. import models

class LicenseViewSet(NetBoxModelViewSet):
    """API view for managing Licenses"""
    queryset = models.License.objects.all()
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilterSet

class LicenseAssignmentViewSet(NetBoxModelViewSet):
    """API viewset for managing LicenseAssignments"""
    queryset = models.LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
    filterset_class = licenseassignments.LicenseAssignmentFilterSet

class LicenseTypeViewSet(NetBoxModelViewSet):
    """API viewset for managing License Types"""
    queryset = models.LicenseType.objects.all()
    serializer_class = LicenseTypeSerializer
    filterset_class = licensetypes.LicenseTypeFilterSet