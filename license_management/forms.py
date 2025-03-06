from django import forms
from .models import License, LicenseAssignment
from dcim.models import Manufacturer  # Import NetBox Manufacturer model

class LicenseForm(forms.ModelForm):
    """Form for adding/editing a software license"""

    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(), 
        required=True,
        label="Manufacturer",
    )

    class Meta:
        model = License
        fields = [
            "license_key",
            "software_name",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "max_assignments",
            "assignment_type",
            "type",
            "status",
            "comment",
        ]

class LicenseImportForm(forms.ModelForm):
    """Form for importing Licenses in bulk."""
    
    class Meta:
        model = License
        fields = [
            "license_key", "software_name", "description", "manufacturer",
            "purchase_date", "expiry_date", "max_assignments", "assignment_type",
            "type", "status", "comment"
        ]

class LicenseBulkEditForm(forms.ModelForm):
    """Form for bulk editing Licenses."""
    
    class Meta:
        model = License
        fields = [
            "software_name", "description", "manufacturer",
            "purchase_date", "expiry_date", "max_assignments", "assignment_type",
            "type", "status", "comment"
        ]

class LicenseAssignmentForm(forms.ModelForm):
    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "assigned_quantity",
            "status",
            "ticket_number",
            "description",
            "comment"
        ]