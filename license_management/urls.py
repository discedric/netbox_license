from django.urls import include, path
from utilities.urls import get_model_urls
from . import views


urlpatterns = [
    # Licenses
    path('licenses/',include(get_model_urls('license_management', 'license', detail=False))),
    path('licenses/<int:pk>/',include(get_model_urls('license_management', 'license'))),
    path('licenses/<int:pk>/changelog/', views.LicenseChangeLogView.as_view(), name='license_changelog'),
    path('licenses/<int:pk>/journal/', views.LicenseJournalView.as_view(), name='license_journal'),

    # License Assignments 
    path('assignments/',include(get_model_urls('license_management', 'licenseassignment',detail=False))),
    path('assignments/<int:pk>/',include(get_model_urls('license_management', 'licenseassignment'))),
    path('assignments/<int:pk>/changelog/',views.LicenseAssignmentChangeLogView.as_view(),name='licenseassignment_changelog'),
    path('assignments/<int:pk>/journal/', views.LicenseAssignmentJournalView.as_view(), name='licenseassignment_journal'),
]
