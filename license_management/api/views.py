from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import LicenseSerializer, LicenseAssignmentSerializer, LicenseTypeSerializer
from .. import filtersets
from .. import models

class LicenseViewSet(NetBoxModelViewSet):
    """API view for managing Licenses"""
    queryset = models.License.objects.all()
    serializer_class = LicenseSerializer
    filterset_class = filtersets.LicenseFilterSet

class LicenseAssignmentViewSet(NetBoxModelViewSet):
    """API viewset for managing LicenseAssignments"""
    queryset = models.LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
    filterset_class = filtersets.LicenseAssignmentFilterSet

class LicenseTypeViewSet(NetBoxModelViewSet):
    """API viewset for managing License Types"""
    queryset = models.LicenseType.objects.all()
    serializer_class = LicenseTypeSerializer
    filterset_class = filtersets.LicenseTypeFilterSet