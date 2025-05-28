from netbox.views import generic
from utilities.views import register_model_view
from netbox_license.models.licensetype import LicenseType
from .. import tables
from netbox_license.filtersets.licensetypes import LicenseTypeFilterSet
from ..forms.filtersets import LicenseTypeFilterForm
from ..forms.models import LicenseTypeForm
from ..forms.bulk_edit import LicenseTypeBulkEditForm
from ..forms.bulk_import import LicenseTypeImportForm
from django.db.models import Count

__all__ = (
    'LicenseTypeView',
    'LicenseTypeListView',
    'LicenseTypeEditView',
    'LicenseTypeDeleteView',
    'LicenseTypeBulkImportView',
    'LicenseTypeBulkEditView',
    'LicenseTypeBulkDeleteView',
)

# -------------------- Object Views --------------------

@register_model_view(LicenseType)
class LicenseTypeView(generic.ObjectView):
    """View for displaying a single License Type"""
    queryset = LicenseType.objects.all()

@register_model_view(LicenseType, 'list', path='', detail=False)
class LicenseTypeListView(generic.ObjectListView):
    queryset = LicenseType.objects.annotate(license_count=Count('licenses', distinct=True))
    table = tables.LicenseTypeTable
    filterset = LicenseTypeFilterSet
    filterset_form = LicenseTypeFilterForm


@register_model_view(LicenseType, 'add', detail=False)
@register_model_view(LicenseType, 'edit')
class LicenseTypeEditView(generic.ObjectEditView):
    queryset = LicenseType.objects.all()
    form = LicenseTypeForm
    default_return_url = 'plugins:netbox_license:licensetype_list'


@register_model_view(LicenseType, 'delete')
class LicenseTypeDeleteView(generic.ObjectDeleteView):
    queryset = LicenseType.objects.all()
    default_return_url = 'plugins:netbox_license:licensetype_list'

# -------------------- bulk --------------------

@register_model_view(LicenseType, 'bulk_import', path='import', detail=False)
class LicenseTypeBulkImportView(generic.BulkImportView):
    queryset = LicenseType.objects.all()
    model_form = LicenseTypeImportForm


@register_model_view(LicenseType, 'bulk_edit', path='edit', detail=False)
class LicenseTypeBulkEditView(generic.BulkEditView):
    queryset = LicenseType.objects.all()
    filterset = LicenseTypeFilterSet
    table = tables.LicenseTypeTable
    form = LicenseTypeBulkEditForm
    default_return_url = 'plugins:netbox_license:licensetype_list'


@register_model_view(LicenseType, 'bulk_delete', path='delete', detail=False)
class LicenseTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = LicenseType.objects.all()
    table = tables.LicenseTypeTable
    default_return_url = 'plugins:netbox_license:licensetype_list'
