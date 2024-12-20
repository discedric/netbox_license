from django.shortcuts import render
from netbox.views import generic

__all__ = (
    'TestView'
)


class TestView(generic.ObjectView):
        title = 'Testing',
        description = 'This is a testing view with a description',