from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField, SlugField
from utilities.forms.rendering import FieldSet, TabbedGroups
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine
from license_management.models import License, LicenseType, LicenseAssignment, LicenseModel

__all__ = (
    'LicenseForm',
    'LicenseAssignmentForm',
    'LicenseTypeForm',
)

class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
    )

    license_type = DynamicModelChoiceField(
        queryset=LicenseType.objects.all(),
        required=True,
        label="License Type",
        help_text="Select the type of license.",
        selector=True,
        quick_add=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        help_text="Select a parent license if applicable.",
        selector=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    license_key = forms.CharField(required=True, label="License Key")

    purchase_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="Purchase Date")
    expiry_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="Expiry Date")

    comment = CommentField()

    class Meta:
        model = License
        fields = [
            "manufacturer", "license_type", "license_key", "serial_number",
            "description", "volume_limit", "parent_license", "purchase_date",
            "expiry_date", "comment"
        ]


class LicenseTypeForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="Manufacturer",
        selector=True,
        quick_add=True
    )

    volume_type = forms.ChoiceField(
        choices=LicenseType.VOLUME_TYPE_CHOICES,
        required=True,
        label="Volume Type"
    )

    license_model = forms.ModelChoiceField(
        queryset=LicenseModel.objects.all(),
        required=True,
        label="License Model"
    )

    base_license = DynamicModelChoiceField(
        queryset=LicenseType.objects.none(),
        required=False,
        label="Base License",
        help_text="Select a base license if this is an expansion pack.",
        selector=True
    )

    purchase_model = forms.ChoiceField(
        choices=LicenseType.PURCHASE_MODEL_CHOICES,
        required=True,
        label="Purchase Model"
    )

    slug = SlugField(
        required=True,
        label="Slug",
        help_text="URL-friendly identifier",
        slug_source="name",
    )

    comments = CommentField()

    class Meta:
        model = LicenseType
        fields = [
            "name", "slug", "manufacturer", "product_code", "ean_code",
            "volume_type", "license_model", "base_license",
            "purchase_model", "description", "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        license_model_id = self.data.get("license_model") or self.initial.get("license_model")
        if license_model_id:
            try:
                selected_license_model = LicenseModel.objects.get(pk=license_model_id)
                if selected_license_model.slug == "expansion":
                    self.fields["base_license"].queryset = LicenseType.objects.filter(
                        license_model__slug="base"
                    )
                    self.fields["base_license"].required = True
                else:
                    self.fields["base_license"].queryset = LicenseType.objects.none()
                    self.fields["base_license"].required = False
            except (LicenseModel.DoesNotExist, ValueError):
                self.fields["base_license"].queryset = LicenseType.objects.none()
                self.fields["base_license"].required = False
        else:
            self.fields["base_license"].queryset = LicenseType.objects.none()
            self.fields["base_license"].required = False

    def clean(self):
        cleaned_data = super().clean()

        license_model = cleaned_data.get("license_model")
        base_license = cleaned_data.get("base_license")

        if license_model and license_model.slug == "expansion":
            if not base_license:
                self.add_error("base_license", "You must select a base license when the license model is set to 'Expansion Pack'.")
        elif license_model and license_model.slug == "base":
            if base_license:
                self.add_error("base_license", "Base licenses cannot reference another base license.")

        return cleaned_data


class LicenseAssignmentForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.none(),
        required=True,
        label="License",
        selector=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device",
        selector=True
    )

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine",
        selector=True
    )

    comments = CommentField()

    fieldsets = (
        FieldSet("manufacturer", "license", "volume", "description", name="General Information"),
        FieldSet(
            TabbedGroups(
                FieldSet("device", name="Device Assignment"),
                FieldSet("virtual_machine", name="Virtual Machine Assignment"),
            ),
            name="Assignment Type"
        ),
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer", "license", "device", "virtual_machine",
            "volume", "description", "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        manufacturer = (
            self.data.get("manufacturer")
            or self.initial.get("manufacturer")
            or getattr(self.instance, "manufacturer", None)
        )

        if manufacturer:
            self.fields["license"].queryset = License.objects.filter(manufacturer=manufacturer)

        if self.instance.pk:
            for field in ["manufacturer", "license", "device", "virtual_machine"]:
                self.fields[field].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        device = cleaned_data.get("device")
        virtual_machine = cleaned_data.get("virtual_machine")

        if not device and not virtual_machine:
            raise forms.ValidationError(
                "You must assign the license to either a Device or a Virtual Machine."
            )

        if device and virtual_machine:
            raise forms.ValidationError(
                "You can only assign a license to either a Device or a Virtual Machine, not both."
            )

        return cleaned_data

    def save(self, commit=True):
        assignment = super().save(commit=False)

        if self.cleaned_data.get("virtual_machine"):
            assignment.device = None
        elif self.cleaned_data.get("device"):
            assignment.virtual_machine = None

        if commit:
            assignment.save()

        return assignment
