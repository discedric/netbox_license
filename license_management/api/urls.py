from rest_framework.routers import DefaultRouter
from .views import LicenseViewSet, LicenseAssignmentViewSet

router = DefaultRouter()
router.register(r'licenses', LicenseViewSet)
router.register(r'assignments', LicenseAssignmentViewSet)

urlpatterns = router.urls
