from netbox.views import generic
from utilities.views import register_model_view
from django.db.models import OuterRef, Subquery, Sum, Case, When, BooleanField, Value
from django.db.models.functions import Coalesce
from ..models import License, LicenseAssignment
from .. import filtersets, tables
from ..forms.filtersets import LicenseFilterForm
from ..forms.bulk_edit import LicenseBulkEditForm
from ..forms.bulk_import import LicenseImportForm
from ..forms.models import LicenseForm


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

# -------------------- Object Views --------------------

@register_model_view(License)
class LicenseView(generic.ObjectView):
    """View for displaying a single License"""
    queryset = License.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
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
    filterset_form = LicenseFilterForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        assignments_sum = LicenseAssignment.objects.filter(
            license=OuterRef('pk')
        ).values('license').annotate(
            total=Sum('volume')
        ).values('total')

        return qs.annotate(
            is_parent_license_value=Case(
                When(sub_licenses__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_child_license_value=Case(
                When(parent_license__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            assigned_count_value=Coalesce(Subquery(assignments_sum), 0)
        ).distinct()



@register_model_view(License, 'edit')
@register_model_view(License, 'add', detail=False)
class LicenseEditView(generic.ObjectEditView):
    """View for creating or editing a license."""
    queryset = License.objects.all()
    form = LicenseForm
    default_return_url = 'plugins:netbox_license:license_list'




@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license"""
    queryset = License.objects.all()

# -------------------- bulk --------------------

@register_model_view(License, 'bulk_import', path='import', detail=False)
class LicenseBulkImportView(generic.BulkImportView):
    """View for bulk importing licenses."""
    queryset = License.objects.all()
    model_form = LicenseImportForm


@register_model_view(License, 'bulk_edit', path='edit', detail=False)
class LicenseBulkEditView(generic.BulkEditView):
    """View for bulk editing licenses."""
    queryset = License.objects.all()
    filterset = filtersets.LicenseFilterSet
    table = tables.LicenseTable
    form = LicenseBulkEditForm
    default_return_url = 'plugins:netbox_license:license_list'


@register_model_view(License, 'bulk_delete', path='delete', detail=False)
class LicenseBulkDeleteView(generic.BulkDeleteView):
    """View for bulk deleting licenses."""
    queryset = License.objects.all()
    table = tables.LicenseTable
