from netbox.views import generic
from utilities.views import register_model_view
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from dcim.models import Device  # Import NetBox Device model
from ..models import License, LicenseAssignment
from .. import filtersets, tables, forms
from django.views.generic import TemplateView

__all__ = (
    'LicenseAssignmentView',
    'LicenseAssignmentListView',
    'LicenseAssignView',
    'LicenseReassignView',
)

@register_model_view(LicenseAssignment)
class LicenseAssignmentView(generic.ObjectView):
    """View to display details of a license assignment."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")

@register_model_view(LicenseAssignment, 'list', path='', detail=False)
class LicenseAssignmentListView(generic.ObjectListView):
    """View to list all assigned licenses."""
    queryset = LicenseAssignment.objects.prefetch_related("license", "device")
    table = tables.LicenseAssignmentTable
    filterset = filtersets.LicenseAssignmentFilterSet

@register_model_view(License, 'assign')
class LicenseAssignView(generic.ObjectEditView):
    """View to assign a license to a device or user/core-based assignment."""
    
    queryset = License.objects.all()
    form = forms.LicenseAssignmentForm
    template_name = "license_management/license_assign.html"

    def get_context_data(self, **kwargs):
        """Manually define get_context_data to provide necessary context."""
        context = super().get_context_data(**kwargs)  # Ensure base class context is included
        context["form"] = kwargs.get("form")  # Form instance
        context["object"] = kwargs.get("object")  # Selected license instance
        context["licenses"] = kwargs.get("licenses", License.objects.all())  # List of available licenses
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET request for license assignment."""
        license_instance = None
        if "pk" in kwargs:
            license_instance = get_object_or_404(License, pk=kwargs["pk"])

        form = self.form(initial={"license": license_instance})
        licenses = License.objects.all()  # Provide a list of licenses to choose from

        context = self.get_context_data(form=form, object=license_instance, licenses=licenses)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle assignment submission."""
        license_instance = None
        if "pk" in kwargs:
            license_instance = get_object_or_404(License, pk=kwargs["pk"])

        form = self.form(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)
            if license_instance:
                assignment.license = license_instance
            else:
                license_instance = form.cleaned_data["license"]

            # Validation logic
            if license_instance.assignment_type == "DEVICES" and not assignment.device:
                form.add_error("device", "A device must be selected for device-based licenses.")
            elif license_instance.assignment_type in ["CORES", "USERS"] and assignment.assigned_quantity <= 0:
                form.add_error("assigned_quantity", "Quantity must be greater than 0 for core/user-based licenses.")

            if form.errors:
                context = self.get_context_data(form=form, object=license_instance)
                return render(request, self.template_name, context)

            assignment.save()
            messages.success(request, "Device/User/Core assigned successfully!")
            return self.redirect(license_instance.get_absolute_url())

        context = self.get_context_data(form=form, object=license_instance)
        return render(request, self.template_name, context)

@register_model_view(License, 'reassign')
class LicenseReassignView(generic.ObjectEditView):
    """View to reassign a license to a different device or user/core-based assignment."""
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

            # Validation logic
            if license_instance.assignment_type == "DEVICES" and not assignment.device:
                form.add_error("device", "A device must be selected for device-based licenses.")
            elif license_instance.assignment_type in ["CORES", "USERS"] and assignment.assigned_quantity <= 0:
                form.add_error("assigned_quantity", "Quantity must be greater than 0 for core/user-based licenses.")

            if form.errors:
                context = self.get_context_data(form=form, object=license_instance)
                return render(request, self.template_name, context)

            assignment.save()
            messages.success(request, "License successfully reassigned!")
            return self.redirect(license_instance.get_absolute_url())

        context = self.get_context_data(form=form, object=license_instance)
        return render(request, self.template_name, context)
