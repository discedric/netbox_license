from django.urls import include, path
from utilities.urls import get_model_urls

from .views import (
    license_views, license_edit_views, license_bulk_views,
    license_assign_views, assignment_views
)
from .views.license_views import LicenseListView, LicenseDetailView, LicenseDeleteView, LicenseChangeLogView
from .views.assignment_views import LicenseAssignmentListView, LicenseAssignmentDetailView
from .views.license_assign_views import LicenseAssignView, LicenseReassignView
from .views.license_bulk_views import LicenseBulkImportView, LicenseBulkEditView, LicenseBulkDeleteView


urlpatterns = (

    path('api/', include('license_management.api.urls')),

    # Licenses
    path('licenses/', LicenseListView.as_view(), name='license_list'),
    path('licenses/add/', license_edit_views.LicenseEditView.as_view(), name='license_add'),
    path('licenses/<int:pk>/', LicenseDetailView.as_view(), name='license'),
    path('licenses/<int:pk>/changelog/', LicenseChangeLogView.as_view(), name='license_changelog'),  # <-- Added this line

    # License Assignments
    path('assignments/', LicenseAssignmentListView.as_view(), name='list_assignments'),
    path('assignments/add/', assignment_views.LicenseAssignmentEditView.as_view(), name='assignment_add'),
    path('assignments/<int:pk>/', LicenseAssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/<int:pk>/edit/', assignment_views.LicenseAssignmentEditView.as_view(), name='assignment_edit'),
    path('assignments/<int:pk>/delete/', assignment_views.LicenseAssignmentDeleteView.as_view(), name='assignment_delete'),

    # Additional License Actions
    path('licenses/<int:pk>/assign/', license_assign_views.LicenseAssignView.as_view(), name='license_assign'),
    path('licenses/<int:pk>/reassign/', license_assign_views.LicenseReassignView.as_view(), name='license_reassign'),
    path('licenses/<int:pk>/edit/', license_edit_views.LicenseEditView.as_view(), name='license_edit'),
    path('licenses/<int:pk>/delete/', license_views.LicenseDeleteView.as_view(), name='license_delete'),

    # Bulk Actions
    path('licenses/import/', license_bulk_views.LicenseBulkImportView.as_view(), name='license_import'),
    path('licenses/bulk-edit/', license_bulk_views.LicenseBulkEditView.as_view(), name='license_bulk_edit'),
    path('licenses/bulk-delete/', license_bulk_views.LicenseBulkDeleteView.as_view(), name='license_bulk_delete'),
)
