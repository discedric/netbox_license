from netbox.views import generic
from utilities.views import register_model_view
from ..models import License
from .. import filtersets, tables
from netbox.views.generic import ObjectChangeLogView
from license_management.models import License
from netbox.views.generic import ObjectView


__all__ = (
    'LicenseView',
    'LicenseListView',
    'LicenseDetailView',
    'LicenseDeleteView',
)

class LicenseDetailView(ObjectView):
    queryset = License.objects.all()
    template_name = "generic/object.html"
    
@register_model_view(License, 'changelog')
class LicenseChangeLogView(ObjectChangeLogView):
    """View for displaying the changelog of a License object"""
    model = License
    template_name = "generic/object_changelog.html"

@register_model_view(License)
class LicenseView(generic.ObjectView):
    """View for displaying a single License."""
    queryset = License.objects.all()


@register_model_view(License, 'list', path='', detail=False)
class LicenseListView(generic.ObjectListView):
    """View for displaying a list of Licenses."""
    queryset = License.objects.all()
    table = tables.LicenseTable
    filterset = filtersets.LicenseFilterSet
    action_buttons = ("add",)


@register_model_view(License, 'detail')
class LicenseDetailView(generic.ObjectView):
    """View for displaying License details."""
    queryset = License.objects.all()


@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license."""
    queryset = License.objects.all()
