from netbox.views import generic
from ..models import License, LicenseAssignment

__all__ = ('TestView', 'Test1View')


class TestView(generic.ObjectView):
    queryset = License.objects.all()


class Test1View(generic.ObjectView):
    queryset = LicenseAssignment.objects.all()
