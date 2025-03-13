from netbox.views import generic
from utilities.views import register_model_view
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from ..models import License
from .. import forms

__all__ = ('LicenseReassignView',)

@register_model_view(License, "reassign")
class LicenseReassignView(generic.ObjectEditView):
    """View to reassign a license."""
    queryset = License.objects.all()
    form = forms.LicenseAssignmentForm
    template_name = "license_management/license_reassign.html"

    def get(self, request, *args, **kwargs):
        """Prefill the license field for reassignment."""
        license_instance = get_object_or_404(License, pk=kwargs.get("pk"))
        form = self.form(initial={"license": license_instance})
        context = self.get_context_data(form=form, object=license_instance)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle reassignment submission."""
        license_instance = get_object_or_404(License, pk=kwargs.get("pk"))
        form = self.form(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.license = license_instance
            assignment.save()
            messages.success(request, "License successfully reassigned!")
            return redirect(license_instance.get_absolute_url())

        context = self.get_context_data(form=form, object=license_instance)
        return render(request, self.template_name, context)
