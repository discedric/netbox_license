from netbox.api.viewsets import NetBoxModelViewSet
from license_management.models import License, LicenseAssignment
from .serializers import LicenseSerializer, LicenseAssignmentSerializer
from rest_framework.permissions import IsAuthenticated

class LicenseViewSet(NetBoxModelViewSet):
    """API view for managing Licenses"""
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Allow filtering by manufacturer."""
        queryset = super().get_queryset()
        manufacturer_id = self.request.query_params.get("manufacturer_id")
        if manufacturer_id:
            queryset = queryset.filter(manufacturer_id=manufacturer_id)
        return queryset
    
class LicenseAssignmentViewSet(NetBoxModelViewSet):
    """API viewset for managing LicenseAssignments"""
    queryset = LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
