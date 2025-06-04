from netbox.views import generic
from utilities.views import register_model_view
from netbox_license.models.licenseassignment import LicenseAssignment
from .. import tables
from netbox_license.filtersets.licenseassignments import LicenseAssignmentFilterSet
from ..forms.models import LicenseAssignmentForm
from ..forms.bulk_edit import LicenseAssignmentBulkEditForm
from ..forms.bulk_import import LicenseAssignmentImportForm
from ..forms.filtersets import LicenseAssignmentFilterForm


__all__ = (
    'LicenseAssignmentListView',
    'LicenseAssignmentView',
    'LicenseAssignmentEditView',
    'LicenseAssignmentDeleteView',

)

# -------------------- Object Views --------------------
@register_model_view(LicenseAssignment)
class LicenseAssignmentView(generic.ObjectView):
    """View to display details of a license assignment."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")

    def get_extra_content(self, request, instance):
        context = super().get_extra_content(request, instance)
        return context


@register_model_view(LicenseAssignment, 'list', path='', detail=False)
class LicenseAssignmentListView(generic.ObjectListView):
    """View to list all assigned licenses with advanced filters."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")
    table = tables.LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet
    filterset_form = LicenseAssignmentFilterForm 

@register_model_view(LicenseAssignment, 'edit')
@register_model_view(LicenseAssignment, 'add', detail=False)
class LicenseAssignmentEditView(generic.ObjectEditView):
    """View to create or edit a license assignment."""
    queryset = LicenseAssignment.objects.all()
    form = LicenseAssignmentForm
    default_return_url = 'plugins:netbox_license:licenseassignment_list'



@register_model_view(LicenseAssignment, 'delete')
class LicenseAssignmentDeleteView(generic.ObjectDeleteView):
    """View to delete a license assignment."""
    queryset = LicenseAssignment.objects.all()
    default_return_url = 'plugins:netbox_license:licenseassignment_list'

# -------------------- bulk --------------------

@register_model_view(LicenseAssignment, 'bulk_import', path='import', detail=False)
class LicenseAssignmentBulkImportView(generic.BulkImportView):
    """View for bulk importing license assignments."""
    queryset = LicenseAssignment.objects.all()
    model_form = LicenseAssignmentImportForm

@register_model_view(LicenseAssignment, 'bulk_edit', path='edit', detail=False)
class LicenseAssignmentBulkEditView(generic.BulkEditView):
    """View for bulk editing license assignments."""
    queryset = LicenseAssignment.objects.all()
    filterset = LicenseAssignmentFilterSet
    table = tables.LicenseAssignmentTable
    form = LicenseAssignmentBulkEditForm
    default_return_url = 'plugins:netbox_license:licenseassignment_list'

@register_model_view(LicenseAssignment, 'bulk_delete', path='delete', detail=False)
class LicenseAssignmentBulkDeleteView(generic.BulkDeleteView):
    """View for bulk deleting license assignments."""
    queryset = LicenseAssignment.objects.all()
    table = tables.LicenseAssignmentTable
    default_return_url = 'plugins:netbox_license:licenseassignment_list'
