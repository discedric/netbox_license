from django.urls import include, path
from utilities.urls import get_model_urls

from .views import license_views, license_edit_views, license_bulk_views, license_assign_views

from .views.license_views import LicenseListView, LicenseDetailView, LicenseDeleteView, LicenseChangeLogView
from .views.license_assign_views import (
    LicenseAssignView, LicenseReassignView, LicenseAssignmentListView, LicenseAssignmentView
)
from .views.license_bulk_views import LicenseBulkImportView, LicenseBulkEditView, LicenseBulkDeleteView


urlpatterns = (
    path('api/', include('license_management.api.urls')),

    # Licenses
    path('licenses/', LicenseListView.as_view(), name='license_list'),
    path('licenses/<int:pk>/', LicenseDetailView.as_view(), name='license_detail'),
    path('licenses/add/', license_edit_views.LicenseEditView.as_view(), name='license_add'),
    path('licenses/<int:pk>/edit/', license_edit_views.LicenseEditView.as_view(), name='license_edit'),
    path('licenses/<int:pk>/delete/', LicenseDeleteView.as_view(), name='license_delete'),
    path('licenses/<int:pk>/changelog/', LicenseChangeLogView.as_view(), name='license_changelog'),

    # License Assignments
    path('assignments/', LicenseAssignmentListView.as_view(), name='list_assignments'),
    path('assignments/add/', LicenseAssignView.as_view(), name='assignment_add'),
    path('assignments/<int:pk>/', LicenseAssignmentView.as_view(), name='assignment_detail'),
    path('assignments/<int:pk>/edit/', LicenseReassignView.as_view(), name='assignment_edit'),
    path('assignments/<int:pk>/delete/', LicenseDeleteView.as_view(), name='assignment_delete'),  # Fixed

    # Additional License Actions
    path('licenses/<int:pk>/assign/', LicenseAssignView.as_view(), name='license_assign'),
    path('licenses/<int:pk>/reassign/', LicenseReassignView.as_view(), name='license_reassign'),

    # Bulk Actions
    path('licenses/import/', LicenseBulkImportView.as_view(), name='license_import'),
    path('licenses/bulk-edit/', LicenseBulkEditView.as_view(), name='license_bulk_edit'),
    path('licenses/bulk-delete/', LicenseBulkDeleteView.as_view(), name='license_bulk_delete'),
)
