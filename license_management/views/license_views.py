from netbox.views import generic
from utilities.views import register_model_view
from ..models import License
from .. import filtersets, tables

__all__ = (
    'LicenseView',
    'LicenseListView',
    'LicenseDetailView',
)


@register_model_view(License)
class LicenseView(generic.ObjectView):
    """View for displaying a single License."""
    queryset = License.objects.all()


@register_model_view(License, 'list', path='', detail=False)
class LicenseListView(generic.ObjectListView):
    """View for displaying a list of Licenses."""
    queryset = License.objects.prefetch_related('owner')
    table = tables.LicenseTable
    filterset = filtersets.LicenseFilterSet
    template_name = "license_management/license.html"


@register_model_view(License, 'detail')
class LicenseDetailView(generic.ObjectView):
    """View for displaying License details."""
    queryset = License.objects.all()

@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license."""
    queryset = License.objects.all()