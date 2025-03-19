from django.urls import include, path
from utilities.urls import get_model_urls
from .views.license_bulk_views import (LicenseAssignmentBulkDeleteView,LicenseAssignmentBulkEditView, LicenseAssignmentBulkImportView)
from .views.license_assignment_views import (
    LicenseAssignmentListView,
    LicenseAssignmentEditView,
    LicenseAssignmentView,
    LicenseAssignmentDeleteView,
    LicenseAssignmentChangeLogView,
)

app_name = "license_management"

urlpatterns = [
    # Licenses
    path(
        'licenses/',
        include(get_model_urls('license_management', 'license', detail=False)),
    ),
    path(
        'licenses/<int:pk>/',
        include(get_model_urls('license_management', 'license')),
    ),

    # License Assignments 
    path(
        'assignments/',
        LicenseAssignmentListView.as_view(),
        name='licenseassignment_list',
    ),
    path(
        'assignments/<int:pk>/',
        LicenseAssignmentView.as_view(),
        name='assignment_detail',
    ),
    path(
        'assignments/<int:pk>/edit/',
        LicenseAssignmentEditView.as_view(),
        name='licenseassignment_edit',
    ),
    path(
        'assignments/<int:pk>/delete/',
        LicenseAssignmentDeleteView.as_view(),
        name='licenseassignment_delete',
    ),
    path(
        'assignments/add/',
        LicenseAssignmentEditView.as_view(),
        name='licenseassignment_add',
    ),
    path(
        'assignments/<int:pk>/changelog/',
        LicenseAssignmentChangeLogView.as_view(),
        name='licenseassignment_changelog',
    ),

    path(
        'assignments/import/',
        LicenseAssignmentBulkImportView.as_view(),
        name='licenseassignment_bulk_import',
    ),
    path(
        'assignments/edit/',
        LicenseAssignmentBulkEditView.as_view(),
        name='licenseassignment_bulk_edit',
    ),
    path(
        'assignments/delete/',
        LicenseAssignmentBulkDeleteView.as_view(),
        name='licenseassignment_bulk_delete',
    ),

    # API
    path("api/", include("license_management.api.urls")),
]
