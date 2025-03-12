from netbox.views import generic
from utilities.views import register_model_view
from ..models import License
from .. import forms

__all__ = (
    'LicenseEditView',
)


@register_model_view(License, 'edit')
@register_model_view(License, 'add', detail=False)
class LicenseEditView(generic.ObjectEditView):
    """View for creating or editing a license."""
    queryset = License.objects.all()
    form = forms.LicenseForm
    
def get_return_url(self, request, obj):
        return obj.get_absolute_url() 

@register_model_view(License, 'delete')
class LicenseDeleteView(generic.ObjectDeleteView):
    """View for deleting a license."""
    queryset = License.objects.all()