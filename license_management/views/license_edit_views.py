from netbox.views import generic
from utilities.views import register_model_view
from ..models import License
from .. import forms

__all__=(
'LicenseEditView',
'LicenseDeleteView',
)

@register_model_view(License, 'edit')
@register_model_view(License, 'add', detail=False)
class LicenseEditView(generic.ObjectEditView):
    """View for creating or editing a license."""
    queryset = License.objects.all()
    form = forms.LicenseForm

    def get_form(self, request, obj=None, **kwargs):
        """Filter manufacturers for quick add and apply filtering logic."""
        form = super().get_form(request, obj, **kwargs)

        manufacturer_id = request.POST.get("manufacturer") or (obj.manufacturer.pk if obj else None)
        
        if manufacturer_id:
            form.fields["parent_license"].queryset = License.objects.filter(manufacturer_id=manufacturer_id)

        return form


@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license."""
    queryset = License.objects.all()