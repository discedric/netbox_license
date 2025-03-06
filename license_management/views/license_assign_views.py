from netbox.views import generic
from utilities.views import register_model_view
from ..models import LicenseAssignment
from .. import filtersets, tables, forms

__all__ = (
    'LicenseAssignmentView',
    'LicenseAssignmentListView',
    'LicenseAssignView',
)


@register_model_view(LicenseAssignment)
class LicenseAssignmentView(generic.ObjectView):
    """View to display details of a license assignment."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")


@register_model_view(LicenseAssignment, 'list', path='', detail=False)
class LicenseAssignmentListView(generic.ObjectListView):
    """View to list all assigned licenses."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")
    table = tables.LicenseAssignmentTable
    filterset = filtersets.LicenseAssignmentFilterSet


@register_model_view(LicenseAssignment, 'assign')
class LicenseAssignView(generic.ObjectEditView):
    """View to assign a license to a device."""
    queryset = LicenseAssignment.objects.all()
    form = forms.LicenseAssignmentForm

@register_model_view(LicenseAssignment, 'reassign')
class LicenseReassignView(generic.ObjectEditView):
    """View to reassign a license to a different device."""
    queryset = LicenseAssignment.objects.all()
    form = forms.LicenseAssignmentForm