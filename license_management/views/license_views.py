from netbox.views import generic
from utilities.views import register_model_view
from django.shortcuts import get_object_or_404
from ..models import License, LicenseAssignment
from .. import filtersets, tables
from netbox.views.generic import ObjectChangeLogView, ObjectView


__all__ = (
    'LicenseView',
    'LicenseListView',
    'LicenseDetailView',
    'LicenseDeleteView',
)
    
@register_model_view(License, 'changelog')
class LicenseChangeLogView(ObjectChangeLogView):
    """View for displaying the changelog of a License object"""
    model = License
    template_name = "generic/object_changelog.html"


@register_model_view(License)
class LicenseView(generic.ObjectView):
    """View for displaying a single License using NetBox's default template."""
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
    """View for displaying License details along with assigned devices using NetBox's default template."""
    queryset = License.objects.prefetch_related("assignments__device")

    def get_extra_context(self, request, instance):
        """Add assigned devices to the context for rendering in NetBox's default template."""
        assigned_devices = instance.assignments.all()

        return {
            "assigned_devices": assigned_devices,
        }


@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license."""
    queryset = License.objects.all()
