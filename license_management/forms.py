from django import forms
from .models import License, LicenseAssignment
from dcim.models import Manufacturer, Device


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
            "product_key",
            "serial_number",
            "software_name",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "assignment_type",
            "volume_limit",
            "parent_license",
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
            if not volume_limit or volume_limit < 2:
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
            "software_name",
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
            "software_name",
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

    class Meta:
        model = LicenseAssignment
        fields = ["license", "device", "volume", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initially disable the volume field until a license is selected
        self.fields["volume"].widget.attrs["disabled"] = True
        self.fields["volume"].required = False

        if "license" in self.data:
            try:
                license_id = int(self.data.get("license"))
                license_instance = License.objects.get(pk=license_id)

                if license_instance.assignment_type == "SINGLE":
                    self.fields["volume"].initial = 1
                    self.fields["volume"].widget.attrs["readonly"] = True
                    self.fields["volume"].widget.attrs["disabled"] = False
                    self.fields["volume"].required = True

                elif license_instance.assignment_type == "VOLUME":
                    self.fields["volume"].widget.attrs.update({"min": 1})
                    self.fields["volume"].widget.attrs["disabled"] = False
                    self.fields["volume"].required = True

                elif license_instance.assignment_type == "UNLIMITED":
                    self.fields["volume"].initial = 1
                    self.fields["volume"].widget.attrs["readonly"] = True
                    self.fields["volume"].widget.attrs["disabled"] = False
                    self.fields["volume"].required = False

            except (ValueError, License.DoesNotExist):
                pass  # Invalid input; leave default behavior.

        elif self.instance.pk and self.instance.license:
            license_instance = self.instance.license
            if license_instance.assignment_type == "SINGLE":
                self.fields["volume"].initial = 1
                self.fields["volume"].widget.attrs["readonly"] = True
                self.fields["volume"].widget.attrs["disabled"] = False
                self.fields["volume"].required = True
            elif license_instance.assignment_type == "VOLUME":
                self.fields["volume"].widget.attrs.update({"min": 1})
                self.fields["volume"].widget.attrs["disabled"] = False
                self.fields["volume"].required = True
            elif license_instance.assignment_type == "UNLIMITED":
                self.fields["volume"].initial = 1
                self.fields["volume"].widget.attrs["readonly"] = True
                self.fields["volume"].widget.attrs["disabled"] = False
                self.fields["volume"].required = False

        # Always populate device choices from existing devices
        self.fields["device"].queryset = Device.objects.all()
