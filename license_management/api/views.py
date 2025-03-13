from netbox.api.viewsets import NetBoxModelViewSet
from license_management.models import License, LicenseAssignment
from .serializers import LicenseSerializer, LicenseAssignmentSerializer

class LicenseViewSet(NetBoxModelViewSet):
    """API viewset for managing Licenses"""
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

class LicenseAssignmentViewSet(NetBoxModelViewSet):
    """API viewset for managing LicenseAssignments"""
    queryset = LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
