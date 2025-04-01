from license_management.api.serializers.licenses import LicenseSerializer
from netbox.views import generic
from utilities.views import register_model_view
from ..models import License
from .. import filtersets, tables, forms

__all__ = (
    'LicenseView',
    'LicenseListView',
    'LicenseChangeLogView',
    'LicenseJournalView',
    'LicenseEditView',
    'LicenseDeleteView',
    'LicenseBulkImportView',
    'LicenseBulkEditView',
    'LicenseBulkDeleteView',
)

@register_model_view(License)
class LicenseView(generic.ObjectView):
    """View for displaying a single License"""
    queryset = License.objects.all()

    def get_extra_content(self, request, instance):
        context = super().get_extra_content(request, instance)
        return context


class LicenseChangeLogView(generic.ObjectChangeLogView):
    """View for displaying the changelog of a License object"""
    queryset = License.objects.all()
    model = License

    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)


class LicenseJournalView(generic.ObjectJournalView):
    """View for displaying the journal of a License object"""
    queryset = License.objects.all()
    model = License

    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)


@register_model_view(License, 'list', path='', detail=False)
class LicenseListView(generic.ObjectListView):
    """View for displaying a list of Licenses"""
    queryset = License.objects.all()
    table = tables.LicenseTable
    filterset = filtersets.LicenseFilterSet
    filterset_form = forms.LicenseFilterForm


@register_model_view(License, 'edit')
@register_model_view(License, 'add', detail=False)
class LicenseEditView(generic.ObjectEditView):
    """View for creating or editing a license."""
    queryset = License.objects.all()
    form = forms.LicenseForm
    default_return_url = 'plugins:license_management:license_list'


@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license"""
    queryset = License.objects.all()


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
    default_return_url = 'plugins:license_management:license_list'


@register_model_view(License, 'bulk_delete', path='delete', detail=False)
class LicenseBulkDeleteView(generic.BulkDeleteView):
    """View for bulk deleting licenses."""
    queryset = License.objects.all()
    table = tables.LicenseTable
