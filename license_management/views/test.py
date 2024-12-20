from django.shortcuts import render
from netbox.views import generic
from ..models import SoftwareLicense

__all__ = (
    'TestView'
)


class TestView(generic.ObjectView):
        queryset = SoftwareLicense.objects.all()