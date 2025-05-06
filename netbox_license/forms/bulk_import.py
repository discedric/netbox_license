from django import forms
from netbox_license import models
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVChoiceField, CSVModelChoiceField
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine
from django.utils.text import slugify
from netbox_license.models import License, LicenseType, LicenseAssignment
from ..choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
    VolumeRelationChoices,
    LicenseStatusChoices,
    LicenseAssignmentStatusChoices,
    AssignmentKindChoices,
)
# ---------- LicenseType ----------

class LicenseTypeImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        required=True,
        help_text='Manufacturer of the license type.'
    )
    slug = forms.SlugField(
        required=True,
        help_text="Unique slug for the license type. Must be URL-safe (letters, numbers, hyphens)."
    )
    license_model = CSVChoiceField(
        choices=LicenseModelChoices,
        required=True,
        help_text='Base license or expansion pack.'
    )
    volume_type = CSVChoiceField(
        choices=VolumeTypeChoices,
        required=True,
        help_text='Type of volume: single, volume, or unlimited.'
    )
    volume_relation = CSVChoiceField(
        choices=VolumeRelationChoices,
        required=False,
        help_text='Optional volume relation type, e.g., CPU, cores, users.'
    )
    purchase_model = CSVChoiceField(
        choices=PurchaseModelChoices,
        required=True,
        help_text='Peripheral or subscription.'
    )
    base_license = CSVModelChoiceField(
        queryset=LicenseType.objects.filter(license_model=LicenseModelChoices.BASE),
        to_field_name='name',
        required=False,
        help_text='Only for expansion licenses. Must reference a base license.'
    )
    comments = forms.CharField(
        required=False,
        help_text='Optional comment on this license type.'
    )

    class Meta:
        model = LicenseType
        fields = [
            "name",
            "slug",
            "manufacturer",
            "product_code",
            "ean_code",
            "volume_type",
            "volume_relation",
            "license_model",
            "base_license",
            "purchase_model",
            "description",
            "comments",
        ]

    def clean_license_model(self):
        license_model = self.cleaned_data.get('license_model').lower()
        if license_model not in LicenseModelChoices.values():
            raise forms.ValidationError(
                f"Invalid license model '{license_model}'. "
                f"Allowed values: {', '.join(LicenseModelChoices.values())}."
            )
        return license_model

    def clean_volume_type(self):
        volume_type = self.cleaned_data.get('volume_type').lower()
        if volume_type not in VolumeTypeChoices.values():
            raise forms.ValidationError(
                f"Invalid volume type '{volume_type}'. "
                f"Allowed values: {', '.join(VolumeTypeChoices.values())}."
            )
        return volume_type
    
    def clean_volume_relation(self):
        volume_relation = self.cleaned_data.get('volume_relation')
        if volume_relation and volume_relation.lower() not in VolumeRelationChoices.values():
            raise forms.ValidationError(
                f"Invalid volume relation '{volume_relation}'. "
                f"Allowed values: {', '.join(VolumeRelationChoices.values())}."
            )
        return volume_relation.lower() if volume_relation else None


    def clean_purchase_model(self):
        purchase_model = self.cleaned_data.get('purchase_model').lower()
        if purchase_model not in PurchaseModelChoices.values():
            raise forms.ValidationError(
                f"Invalid purchase model '{purchase_model}'. "
                f"Allowed values: {', '.join(PurchaseModelChoices.values())}."
            )
        return purchase_model

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            return

        license_model = cleaned_data.get('license_model')
        base_license = cleaned_data.get('base_license')

        if license_model == LicenseModelChoices.EXPANSION:
            if not base_license:
                self.add_error('base_license', "Expansion licenses must reference a base license.")
            elif base_license.license_model != LicenseModelChoices.BASE:
                self.add_error('base_license', "The referenced base license must be of type 'Base License'.")
        elif license_model == LicenseModelChoices.BASE:
            if base_license:
                self.add_error('base_license', "Base licenses cannot reference another base license.")

        name = cleaned_data.get('name')
        if name:
            generated_slug = slugify(name)
            if LicenseType.objects.filter(slug=generated_slug).exists():
                self.add_error('name', f"A License Type with the generated slug '{generated_slug}' already exists.")
            else:
                self.instance.slug = generated_slug

        return cleaned_data


    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.fields['base_license'].queryset = LicenseType.objects.filter(
            license_model=LicenseModelChoices.BASE
        )

    def _clean_fields(self):
        """
        This step ensures all fields are validated properly and converted to lowercase where needed.
        """
        if self.data:
            mutable_data = self.data.copy()
            for field in ['license_model', 'volume_type', 'purchase_model']:
                if mutable_data.get(field):
                    mutable_data[field] = mutable_data[field].strip().lower()
            self.data = mutable_data
        return super()._clean_fields()


# ---------- License ----------

class LicenseImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        required=True,
        help_text='Manufacturer of the license.'
    )

    license_type = CSVModelChoiceField(
        queryset=LicenseType.objects.all(),
        to_field_name='name',
        label='License Type',
        help_text='Name of the license type'
    )

    license_key = forms.CharField(
        required=True,
        help_text='Unique license key'
    )

    serial_number = forms.CharField(
        required=False,
        help_text='Serial number of the license'
    )

    description = forms.CharField(
        required=False,
        help_text='Additional description or notes'
    )

    purchase_date = forms.DateField(
        required=False,
        help_text='Date when the license was purchased'
    )

    expiry_date = forms.DateField(
        required=False,
        help_text='Expiration date of the license'
    )

    volume_limit = forms.IntegerField(
        required=False,
        help_text='Required if license type is "Volume". Must be 2 or more.'
    )

    parent_license = CSVModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        to_field_name='license_key',
        help_text='Parent license key if applicable'
    )
    comments = forms.CharField(
        required=False,
        help_text='Optional comment on this license.'
    )

    class Meta:
        model = License
        fields = [
            "manufacturer", "license_type", "license_key", "serial_number", "description",
            "purchase_date", "expiry_date", "volume_limit", "parent_license", "comments",
        ]

    def clean(self):
        super().clean()

        license_type = self.cleaned_data.get("license_type")
        if license_type:
            self.instance.manufacturer = license_type.manufacturer

            vt = license_type.volume_type
            volume_limit = self.cleaned_data.get("volume_limit")

            if vt == "SINGLE":
                if volume_limit and volume_limit != 1:
                    raise forms.ValidationError({
                        "volume_limit": "Single licenses must have a volume limit of exactly 1."
                    })
                self.cleaned_data["volume_limit"] = 1

            elif vt == "UNLIMITED":
                self.cleaned_data["volume_limit"] = None

            elif vt == "VOLUME":
                if not volume_limit or volume_limit < 2:
                    raise forms.ValidationError({
                        "volume_limit": "Volume licenses require a volume limit of at least 2."
                    })

            parent_license = self.cleaned_data.get("parent_license")

            if license_type.license_model == "expansion":
                if not parent_license:
                    raise forms.ValidationError({
                        "parent_license": "Expansion licenses must reference a parent base license."
                    })
                if parent_license.license_type.license_model != "base":
                    raise forms.ValidationError({
                        "parent_license": "The selected parent license must be of license model 'Base'."
                    })

            elif license_type.license_model == "base" and parent_license:
                raise forms.ValidationError({
                    "parent_license": "Base licenses cannot reference a parent license."
                })

        purchase = self.cleaned_data.get("purchase_date")
        expiry = self.cleaned_data.get("expiry_date")
        if purchase and expiry and expiry < purchase:
            raise forms.ValidationError({
                "expiry_date": "Expiry date cannot be earlier than purchase date."
            })

# ---------- Assignments ----------

class LicenseAssignmentImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer.'
    )

    license = CSVModelChoiceField(
        queryset=License.objects.all(),
        to_field_name='license_key',
        label='License',
        help_text='The license key to assign.'
    )

    model_kind = CSVChoiceField(
        choices=AssignmentKindChoices,
        required=True,
        label='Kind',
        help_text='Type of object to assign the license to (device or virtual_machine).'
    )

    model_name = forms.CharField(
        required=True,
        label='Object Name',
        help_text='Name of the Device or Virtual Machine to assign.'
    )

    volume = forms.IntegerField(
        required=True,
        min_value=1,
        label='Volume',
        help_text='Amount of license assigned.'
    )

    description = forms.CharField(
        required=False,
        label='Description',
        help_text='Optional description of the assignment.'
    )

    comments = forms.CharField(
        required=False,
        label='Comments',
        help_text='Optional comments about this assignment.'
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer",
            "license",
            "model_kind",
            "model_name",
            "volume",
            "description",
            "comments",
        ]

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        if 'device' in exclude:
            exclude.remove('device')
        if 'virtual_machine' in exclude:
            exclude.remove('virtual_machine')
        return exclude

    def clean_model_name(self):
        kind = self.cleaned_data.get("model_kind")
        name = self.cleaned_data.get("model_name")

        if not kind or not name:
            raise forms.ValidationError("Both 'model_kind' and 'model_name' are required.")

        try:
            if kind == AssignmentKindChoices.DEVICE:
                device = Device.objects.get(name=name)
                setattr(self.instance, "device", device)
                setattr(self.instance, "virtual_machine", None)
            elif kind == AssignmentKindChoices.VM:
                vm = VirtualMachine.objects.get(name=name)
                setattr(self.instance, "virtual_machine", vm)
                setattr(self.instance, "device", None)
            else:
                raise forms.ValidationError(f"Invalid kind: {kind}. Must be 'device' or 'virtual_machine'.")
        except ObjectDoesNotExist:
            raise forms.ValidationError(f"{kind.capitalize()} '{name}' not found.")

        return name

    def clean_license(self):
        license = self.cleaned_data.get("license")
        if license is None:
            raise forms.ValidationError("License Key not found. Make sure the license exists.")
        return license


    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        license = cleaned_data.get("license")
        volume = cleaned_data.get("volume")

        license_type = license.license_type
        if not license_type:
            raise forms.ValidationError("License must be linked to a License Type.")

        if license_type.volume_type == "single":
            if volume != 1:
                raise forms.ValidationError("Single licenses must be assigned with a volume of 1.")
            if license.assignments.exists():
                raise forms.ValidationError("Single licenses can only have one assignment.")

        elif license_type.volume_type == "volume":
            total_assigned = license.assignments.aggregate(models.Sum("volume"))["volume__sum"] or 0
            if (total_assigned + volume) > (license.volume_limit or 0):
                raise forms.ValidationError(
                    f"Assigned volume exceeds limit ({license.volume_limit}). Already assigned: {total_assigned}."
                )

        return cleaned_data





