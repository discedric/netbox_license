from django.urls import path

from . import views

urlpatterns = [
    # Test List
    path('licenses/', views.TestView.as_view(), name='test_view'),
]
