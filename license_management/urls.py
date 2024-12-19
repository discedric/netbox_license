from django.urls import path
from . import views

urlpatterns = [
    path('licenses/', views.list_licenses, name='list_licenses'),
]
