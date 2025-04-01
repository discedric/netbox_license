from netbox.views import generic
from utilities.views import register_model_view
from ..models import LicenseType
from .. import filtersets, tables, forms

__all__ = (
    'LicenseTypeView',
    'LicenseTypeListView',
    'LicenseTypeEditView',
    'LicenseTypeDeleteView',
    'LicenseTypeBulkImportView',
    'LicenseTypeBulkEditView',
    'LicenseTypeBulkDeleteView',
    'LicensetypeChangeLogView',
    'LicensetypeJournalView',
)

@register_model_view(LicenseType)
class LicenseTypeView(generic.ObjectView):
    queryset = LicenseType.objects.all()


class LicensetypeChangeLogView(generic.ObjectChangeLogView):
    queryset = LicenseType.objects.all()
    model = LicenseType

    def get(self, request, *args, **kwargs):
        return super().get(request, model=self.model, *args, **kwargs)


class LicensetypeJournalView(generic.ObjectJournalView):
    queryset = LicenseType.objects.all()
    model = LicenseType

    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)



@register_model_view(LicenseType, 'list', path='', detail=False)
class LicenseTypeListView(generic.ObjectListView):
    queryset = LicenseType.objects.all()
    table = tables.LicenseTypeTable
    filterset = filtersets.LicenseTypeFilterSet
    filterset_form = forms.LicenseTypeFilterForm


@register_model_view(LicenseType, 'add', detail=False)
@register_model_view(LicenseType, 'edit')
class LicenseTypeEditView(generic.ObjectEditView):
    queryset = LicenseType.objects.all()
    form = forms.LicenseTypeForm
    default_return_url = 'plugins:license_management:licensetype_list'


@register_model_view(LicenseType, 'delete')
class LicenseTypeDeleteView(generic.ObjectDeleteView):
    queryset = LicenseType.objects.all()


@register_model_view(LicenseType, 'bulk_import', path='import', detail=False)
class LicenseTypeBulkImportView(generic.BulkImportView):
    queryset = LicenseType.objects.all()
    model_form = forms.LicenseTypeImportForm


@register_model_view(LicenseType, 'bulk_edit', path='edit', detail=False)
class LicenseTypeBulkEditView(generic.BulkEditView):
    queryset = LicenseType.objects.all()
    filterset = filtersets.LicenseTypeFilterSet
    table = tables.LicenseTypeTable
    form = forms.LicenseTypeBulkEditForm
    default_return_url = 'plugins:license_management:licensetype_list'


@register_model_view(LicenseType, 'bulk_delete', path='delete', detail=False)
class LicenseTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = LicenseType.objects.all()
    table = tables.LicenseTypeTable
