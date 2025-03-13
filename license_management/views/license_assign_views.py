from netbox.views import generic
from utilities.views import register_model_view
from ..models import License
from .. import forms

__all__ = ('LicenseAssignView',)

@register_model_view(License, "assign")
class LicenseAssignView(generic.ObjectEditView):
    """View to assign a license to a device."""
    queryset = License.objects.all()
    form = forms.LicenseAssignmentForm
    template_name = "license_management/license_assign.html"

    def get_extra_context(self, request, instance):
        """Include assigned devices in the context."""
        assigned_devices = instance.assignments.all() if instance.pk else []
        return {"assigned_devices": assigned_devices}
