from netbox.api.routers import NetBoxRouter
from django.urls import path, include
from .views import LicenseViewSet, LicenseAssignmentViewSet

app_name='license_management'

router = NetBoxRouter()
router.register(r'license', LicenseViewSet)
router.register(r'license-assignments', LicenseAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
