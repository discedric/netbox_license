from django.urls import path
from .views import TestView, Test1View

urlpatterns = [
    path('test/', TestView.as_view(), name='test-view'),
    path('test1/', Test1View.as_view(), name='test1-view'),
]
