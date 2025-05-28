from django.urls import include, path
from utilities.urls import get_model_urls
from . import views


urlpatterns = [
    # Licenses
    path('licenses/',include(get_model_urls('netbox_license', 'license', detail=False))),
    path('licenses/<int:pk>/',include(get_model_urls('netbox_license', 'license'))),

    # License type
    path('types/', include(get_model_urls('netbox_license', 'licensetype', detail=False))),
    path('types/<int:pk>/', include(get_model_urls('netbox_license', 'licensetype'))),

    # License Assignments 
    path('assignments/',include(get_model_urls('netbox_license', 'licenseassignment',detail=False))),
    path('assignments/<int:pk>/',include(get_model_urls('netbox_license', 'licenseassignment'))),
    
]
