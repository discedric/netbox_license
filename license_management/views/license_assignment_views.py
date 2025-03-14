from netbox.views import generic
from utilities.views import register_model_view
from ..models import LicenseAssignment
from .. import filtersets, tables, forms
from netbox.views.generic import ObjectChangeLogView

__all__ = (
    'LicenseAssignmentListView',
    'LicenseAssignmentView',
    'LicenseAssignmentEditView',
    'LicenseAssignmentDeleteView',
    'LicenseAssignmentChangeLogView',
)

@register_model_view(LicenseAssignment, "changelog")
class LicenseAssignmentChangeLogView(ObjectChangeLogView):
    """View for displaying the changelog of a LicenseAssignment object"""
    model = LicenseAssignment
    template_name = "generic/object_changelog.html"


@register_model_view(LicenseAssignment)
class LicenseAssignmentView(generic.ObjectView):
    """View to display details of a license assignment."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")
    template_name = "license_management/license_assignment.html"


@register_model_view(LicenseAssignment, "list", path="", detail=False)
class LicenseAssignmentListView(generic.ObjectListView):
    """View to list all assigned licenses."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")
    table = tables.LicenseAssignmentTable
    filterset = filtersets.LicenseAssignmentFilterSet
    action_buttons = ("add", "export")


@register_model_view(LicenseAssignment, 'edit')
@register_model_view(LicenseAssignment, 'add', detail=False)
class LicenseAssignmentEditView(generic.ObjectEditView):
    """View to create or edit a license assignment."""
    queryset = LicenseAssignment.objects.all()
    form = forms.LicenseAssignmentForm


@register_model_view(LicenseAssignment, 'delete')
class LicenseAssignmentDeleteView(generic.ObjectDeleteView):
    """View to delete a license assignment."""
    queryset = LicenseAssignment.objects.all()


