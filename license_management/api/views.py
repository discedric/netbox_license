from netbox.api.viewsets import NetBoxModelViewSet
from license_management.models import License
from .serializers import LicenseSerializer

class LicenseViewSet(NetBoxModelViewSet):
    """API viewset for managing Licenses"""
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
