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
        fields = ["license", "device", "assigned_quantity", "status"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        license_instance = self.instance.license if self.instance.pk else None

        if license_instance:
            if license_instance.assignment_type == "DEVICES":
                self.fields["device"].queryset = Device.objects.all()
            else:
                del self.fields["device"]

            if license_instance.assignment_type in ["CORES", "USERS"]:
                self.fields["assigned_quantity"].widget = forms.NumberInput(attrs={"min": 1})
            else:
                del self.fields["assigned_quantity"]