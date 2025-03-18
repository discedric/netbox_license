from netbox.views import generic
from utilities.views import register_model_view
from ..models import License, LicenseAssignment
from .. import filtersets, tables, forms


__all__ = (
    'LicenseAssignmentListView',
    'LicenseAssignmentView',
    'LicenseAssignmentEditView',
    'LicenseAssignmentDeleteView',
    'LicenseAssignmentChangeLogView',
)


class LicenseAssignmentChangeLogView(generic.ObjectChangeLogView):
    queryset = LicenseAssignment.objects.all()
    model = LicenseAssignment
    template_name = "extras/object_changelog.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, model=self.model, *args, **kwargs) 

@register_model_view(LicenseAssignment)
class LicenseAssignmentView(generic.ObjectView):
    """View to display details of a license assignment."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")
    template_name = "license_management/licenseassignment.html"


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

    def get_form(self, request, obj=None, **kwargs):
        """Filter licenses based on the selected manufacturer."""
        form = super().get_form(request, obj, **kwargs)

        manufacturer_id = request.POST.get("manufacturer") or (obj.manufacturer.pk if obj else None)
        if manufacturer_id:
            form.fields["license"].queryset = License.objects.filter(manufacturer_id=manufacturer_id)

        return form

@register_model_view(LicenseAssignment, 'delete')
class LicenseAssignmentDeleteView(generic.ObjectDeleteView):
    """View to delete a license assignment."""
    queryset = LicenseAssignment.objects.all()
