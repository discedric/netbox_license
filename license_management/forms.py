from django import forms
from .models import License, LicenseAssignment
from dcim.models import Manufacturer, Device
from utilities.forms.fields import DynamicModelChoiceField

class LicenseFilterForm(forms.Form):
    """Filter form for licenses in object selector"""

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer",
        selector=True
    )

    name = forms.CharField(
        required=False,
        label="License Name"
    )

    def filter_queryset(self, queryset):
        """Apply filters to the queryset based on form data"""
        manufacturer = self.cleaned_data.get("manufacturer")
        name = self.cleaned_data.get("name")

        if manufacturer:
            queryset = queryset.filter(manufacturer=manufacturer)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
    

class LicenseForm(forms.ModelForm):
    """Form for adding/editing a software license"""

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="Manufacturer",
        selector=True, 
        quick_add=True  
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        help_text="Select a parent license if applicable.",
        selector=True,
        query_params={  
            'manufacturer_id': '$manufacturer',  
        }
    )

    license_key = forms.CharField(
        required=True,
        label="License Key"
    )

    name = forms.CharField(
        required=True,
        label="Name"
    )

    assignment_type = forms.ChoiceField(
        choices=License.ASSIGNMENT_TYPE_CHOICES,
        required=True,
        label="Assignment Type"
    )

    purchase_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Purchase Date"
    )

    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Expiry Date"
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Comment"
    )

    class Meta:
        model = License
        fields = [
            "manufacturer",  
            "license_key",
            "product_key",
            "name",
            "serial_number",
            "description",
            "assignment_type",
            "volume_limit",
            "parent_license",
            "purchase_date",
            "expiry_date",
            "comment"  
        ]

    def clean(self):
        cleaned_data = super().clean()
        assignment_type = cleaned_data.get("assignment_type")
        volume_limit = cleaned_data.get("volume_limit")

        if assignment_type == "SINGLE":
            cleaned_data["volume_limit"] = 1
        elif assignment_type == "UNLIMITED":
            cleaned_data["volume_limit"] = None
        elif assignment_type == "VOLUME":
            if volume_limit is None or volume_limit < 2:
                self.add_error("volume_limit", "Volume licenses require a volume limit of at least 2.")

        return cleaned_data


class LicenseImportForm(forms.ModelForm):
    """Form for importing Licenses in bulk."""

    class Meta:
        model = License
        fields = [
            "license_key",
            "product_key",
            "serial_number",
            "name",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "assignment_type",
            "volume_limit",
            "parent_license",
        ]


class LicenseBulkEditForm(forms.ModelForm):
    """Form for bulk editing Licenses."""

    class Meta:
        model = License
        fields = [
            "name",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "assignment_type",
            "volume_limit",
            "parent_license",
        ]




class LicenseAssignmentForm(forms.ModelForm):
    """Form for assigning a License to a Device."""

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="Manufacturer",
        selector=True, 
        quick_add=True  
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=True,
        label="License",
        selector=True,
        query_params={ 
            'manufacturer_id': '$manufacturer',
        }
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        label="Device"
    )

    class Meta:
        model = LicenseAssignment
        fields = ["manufacturer", "license", "device", "volume", "description"]
