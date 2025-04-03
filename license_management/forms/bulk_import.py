from django import forms
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine
from license_management.models import License, LicenseType, LicenseAssignment


class LicenseImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer'
    )

    parent_license = CSVModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        to_field_name='license_key',
        label='Parent License',
        help_text='Parent license key if applicable'
    )

    class Meta:
        model = License
        fields = [
            "license_key",
            "serial_number",
            "description",
            "manufacturer",
            "purchase_date",
            "expiry_date",
            "volume_limit",
            "parent_license"
        ]
        labels = {
            "license_key": "License Key",
            "serial_number": "Serial Number",
            "description": "Description",
            "manufacturer": "Manufacturer",
            "purchase_date": "Purchase Date",
            "expiry_date": "Expiry Date",
            "volume_limit": "Volume Limit",
            "parent_license": "Parent License",
        }
        help_texts = {
            "license_key": "Unique license key",
            "serial_number": "Serial number of the license",
            "description": "Additional notes or description",
            "manufacturer": "Manufacturer of the software/license",
            "purchase_date": "Date when the license was purchased",
            "expiry_date": "Expiration date of the license",
            "volume_limit": "Number of uses (if volume license)",
            "parent_license": "Link to a parent license if this is a child",
        }

    def clean(self):
        super().clean()


class LicenseTypeImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license type manufacturer'
    )

    license_model = CSVModelChoiceField(
        queryset=LicenseModel.objects.all(),
        to_field_name='slug',
        label='License Model',
        help_text='Base license or expansion pack (slug)'
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
            "license_model",
            "purchase_model",
            "description"
        ]
        labels = {
            "name": "Name",
            "slug": "Slug",
            "manufacturer": "Manufacturer",
            "product_code": "Product Code",
            "ean_code": "EAN Code",
            "volume_type": "Volume Type",
            "license_model": "License Model",
            "purchase_model": "Purchase Model",
            "description": "Description",
        }
        help_texts = {
            "name": "Name of the license type",
            "slug": "URL-friendly identifier",
            "manufacturer": "Manufacturer of the license type",
            "product_code": "Internal or external product code",
            "ean_code": "European Article Number",
            "volume_type": "Type of volume: single, volume, or unlimited",
            "license_model": "Base license or expansion pack",
            "purchase_model": "Peripheral or subscription",
            "description": "Optional notes",
        }


class LicenseAssignmentImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer'
    )

    license = CSVModelChoiceField(
        queryset=License.objects.all(),
        to_field_name='license_key',
        label='License',
        help_text='Assigned license (by license key)'
    )

    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name='name',
        required=False,
        label='Device',
        help_text='Device to assign the license to (optional)'
    )

    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        required=False,
        label='Virtual Machine',
        help_text='Virtual machine to assign the license to (optional)'
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer",
            "license",
            "device",
            "virtual_machine",
            "volume",
            "description"
        ]
        labels = {
            "manufacturer": "Manufacturer",
            "license": "License",
            "device": "Device",
            "virtual_machine": "Virtual Machine",
            "volume": "Volume",
            "description": "Description",
        }
        help_texts = {
            "manufacturer": "The license manufacturer",
            "license": "License assigned by license key",
            "device": "Device name (if applicable)",
            "virtual_machine": "VM name (if applicable)",
            "volume": "How many units are assigned",
            "description": "Optional description of the assignment",
        }

    def clean(self):
        super().clean()
        device = self.cleaned_data.get("device")
        virtual_machine = self.cleaned_data.get("virtual_machine")

        if not device and not virtual_machine:
            raise forms.ValidationError(
                "You must assign the license to either a Device or a Virtual Machine."
            )

        if device and virtual_machine:
            raise forms.ValidationError(
                "A license can only be assigned to a Device or a Virtual Machine, not both."
            )
