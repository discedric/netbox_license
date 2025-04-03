from django import forms
from license_management.models import License, LicenseType, LicenseAssignment, LicenseModel

class LicenseBulkEditForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "volume_limit",
            "parent_license",
        ]


class LicenseTypeBulkEditForm(forms.ModelForm):
    class Meta:
        model = LicenseType
        fields = [
            "name",
            "slug",
            "manufacturer",
            "product_code",
            "ean_code",
            "volume_type",
            "license_model",
            "purchase_model",
            "description",
            "comments",
        ]


class LicenseAssignmentBulkEditForm(forms.ModelForm):
    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "volume",
            "description",
        ]
