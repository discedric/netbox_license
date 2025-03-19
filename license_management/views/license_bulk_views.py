from netbox.views import generic
from utilities.views import register_model_view
from ..models import License, LicenseAssignment
from .. import filtersets, forms, tables

__all__ = (
    'LicenseBulkImportView',
    'LicenseBulkEditView',
    'LicenseBulkDeleteView',
    'LicenseAssignmentBulkImportView',
    'LicenseAssignmentBulkEditView',
    'LicenseAssignmentBulkDeleteView',
)
# Views for License bulk

@register_model_view(License, 'bulk_import', path='import', detail=False)
class LicenseBulkImportView(generic.BulkImportView):
    """View for bulk importing licenses."""
    queryset = License.objects.all()
    model_form = forms.LicenseImportForm

@register_model_view(License, 'bulk_edit', path='edit', detail=False)
class LicenseBulkEditView(generic.BulkEditView):
    """View for bulk editing licenses."""
    queryset = License.objects.all()
    filterset = filtersets.LicenseFilterSet
    table = tables.LicenseTable
    form = forms.LicenseBulkEditForm

@register_model_view(License, 'bulk_delete', path='delete', detail=False)
class LicenseBulkDeleteView(generic.BulkDeleteView):
    """View for bulk deleting licenses."""
    queryset = License.objects.all()
    table = tables.LicenseTable

# Views for LicenseAssignment bulk

@register_model_view(LicenseAssignment, 'bulk_import', path='import', detail=False)
class LicenseAssignmentBulkImportView(generic.BulkImportView):
    """View for bulk importing license assignments."""
    queryset = LicenseAssignment.objects.all()
    model_form = forms.LicenseAssignmentImportForm

@register_model_view(LicenseAssignment, 'bulk_edit', path='edit', detail=False)
class LicenseAssignmentBulkEditView(generic.BulkEditView):
    """View for bulk editing license assignments."""
    queryset = LicenseAssignment.objects.all()
    filterset = filtersets.LicenseAssignmentFilterSet
    table = tables.LicenseAssignmentTable
    form = forms.LicenseAssignmentBulkEditForm

@register_model_view(LicenseAssignment, 'bulk_delete', path='delete', detail=False)
class LicenseAssignmentBulkDeleteView(generic.BulkDeleteView):
    """View for bulk deleting license assignments."""
    queryset = LicenseAssignment.objects.all()
    table = tables.LicenseAssignmentTable
