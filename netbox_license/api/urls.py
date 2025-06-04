from netbox.api.routers import NetBoxRouter
from django.urls import path, include
from .views import LicenseViewSet, LicenseAssignmentViewSet, LicenseTypeViewSet

app_name='netbox_license'

router = NetBoxRouter()
router.register(r'licenses', LicenseViewSet)
router.register(r'license-assignments', LicenseAssignmentViewSet)
router.register(r'license-types', LicenseTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
