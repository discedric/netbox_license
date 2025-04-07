from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine
from django.utils.timezone import now
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

class LicenseType(NetBoxModel):
    VOLUME_TYPE_CHOICES = [
        ("SINGLE", "Single "),
        ("VOLUME", "Volume"),
        ("UNLIMITED", "Unlimited"),
    ]

    PURCHASE_MODEL_CHOICES = [
        ("PERIPHERAL", "Peripheral"),
        ("SUBSCRIPTION", "Subscription"),
    ]

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)
    
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="license_types"
    )

    product_code = models.CharField(max_length=255, blank=True, null=True)

    ean_code = models.CharField(max_length=255, blank=True, null=True)

    volume_type = models.CharField(max_length=20, choices=VOLUME_TYPE_CHOICES)

    LICENSE_MODEL_CHOICES = [
        ("BASE", "Base License"),
        ("EXPANSION", "Expansion Pack"),
    ]

    license_model = models.CharField(
        max_length=20,
        choices=LICENSE_MODEL_CHOICES,
        default="BASE"
    )
    base_license = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expansions",
        help_text="Only for expansion licenses. Must reference a base license."
    )
    purchase_model = models.CharField(max_length=20, choices=PURCHASE_MODEL_CHOICES, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    clone_fields = ['manufacturer', 'volume_type', 'license_model', 'purchase_model']

    def clean(self):
        if self.license_model == "EXPANSION":
            if not self.base_license:
                raise ValidationError({"base_license": "An Expansion license type must reference a Base license."})
            if self.base_license.license_model != "BASE":
                raise ValidationError({"base_license": "Base License must be of type 'BASE'."})
        elif self.license_model == "BASE":
            if self.base_license is not None:
                raise ValidationError({"base_license": "Only Expansion licenses can reference a base license."})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:license_management:licensetype", args=[self.pk])

    class Meta:
        verbose_name = "License Type"
        verbose_name_plural = "License Types"


class License(NetBoxModel):
    license_key = models.CharField(max_length=255, unique=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    license_type = models.ForeignKey(
        'LicenseType',
        on_delete=models.PROTECT,
        related_name="licenses"
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="licenses",
        null=True, blank=True,
        help_text="Redundant for filtering; copied from license_type."
    )
    purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    volume_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Required if license type is volume."
    )
    parent_license = models.ForeignKey(
        to='self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_licenses",
        help_text="Link to parent license for extensions."
    )

    def clean(self):
        if self.license_type:
            self.manufacturer = self.license_type.manufacturer

        vt = self.license_type.volume_type if self.license_type else None
        if vt == "SINGLE":
            self.volume_limit = 1
        elif vt == "UNLIMITED":
            self.volume_limit = None
        elif vt == "VOLUME":
            if not self.volume_limit or self.volume_limit < 2:
                raise ValidationError("Volume licenses require a volume limit of at least 2.")

        if self.purchase_date and self.expiry_date:
            if self.expiry_date < self.purchase_date:
                raise ValidationError(_("Expiry date cannot be earlier than purchase date."))

    def current_usage(self):
        assigned = self.assignments.aggregate(models.Sum('volume'))['volume__sum'] or 0
        return assigned

    def usage_display(self):
        vt = self.license_type.volume_type if self.license_type else ""
        if vt == "UNLIMITED":
            return f"{self.current_usage()}/∞"
        return f"{self.current_usage()}/{self.volume_limit}"

    @property
    def is_parent_license(self):
        return self.sub_licenses.exists()

    @property
    def is_child_license(self):
        return self.parent_license is not None

    def __str__(self):
        return f"{self.license_key}"

    def get_absolute_url(self):
        return reverse("plugins:license_management:license", args=[self.pk])

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"

    def get_expiry_progress(self):
        if not self.expiry_date or not self.purchase_date:
            return None

        days_left = (self.expiry_date - date.today()).days

        total_days = (self.expiry_date - self.purchase_date).days
        if total_days <= 0:
            percent = 100
        else:
            percent = int((1 - (days_left / total_days)) * 100)

        if days_left < 0:
            color = "danger"
        elif days_left < 90:
            color = "warning"
        elif days_left < 365:
            color = "info"
        else:
            color = "success"

        return {
            "percent": max(0, min(percent, 100)),
            "days_left": days_left,
            "color": color,
            "expired": days_left < 0,
        }


class LicenseAssignment(NetBoxModel):
    """Represents assignment of a license to a device OR a virtual machine."""

    license = models.ForeignKey(
        "License", on_delete=models.CASCADE, related_name="assignments"
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="license_assignments",
        null=True, blank=True
    )
    virtual_machine = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="license_assignments",
        null=True, blank=True
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.PROTECT, related_name="license_assignments", null=True, blank=True
    )
    volume = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of license allocated. Only relevant for Volume Licenses."
    )
    assigned_to = models.DateTimeField(default=now)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    device_manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="device_license_assignments",
        null=True,
        blank=True
    )

    def clean(self):
        if self.device and self.virtual_machine:
            raise ValidationError("A license can only be assigned to either a Device or a Virtual Machine, not both.")
        if not self.device and not self.virtual_machine:
            raise ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if self.license:
            if not self.license.license_type:
                raise ValidationError("Selected license must be linked to a license type.")

            volume_type = self.license.license_type.volume_type

            self.manufacturer = self.license.manufacturer

            if volume_type == "SINGLE":
                if self.volume != 1:
                    raise ValidationError("Single licenses can only have a volume of 1.")
                existing_assignments = self.license.assignments.exclude(pk=self.pk).count()
                if existing_assignments >= 1:
                    raise ValidationError("Single licenses can only be assigned to one entity (Device or VM).")

            elif volume_type == "VOLUME":
                if self.volume < 1:
                    raise ValidationError("Volume quantity must be at least 1.")
                total_assigned_volume = (
                    self.license.assignments.exclude(pk=self.pk)
                    .aggregate(models.Sum('volume'))['volume__sum'] or 0
                )
                if total_assigned_volume + self.volume > self.license.volume_limit:
                    raise ValidationError(
                        f"Exceeds volume limit ({self.license.volume_limit}). Currently assigned: {total_assigned_volume}."
                    )

        if self.device and not self.device_manufacturer:
            self.device_manufacturer = self.device.device_type.manufacturer

    clone_fields = [
        'manufacturer', 'license', 'device', 'virtual_machine', 'description',
    ]

    def __str__(self):
        return f"{self.license.license_key} → {self.device or self.virtual_machine} ({self.volume})"

    def get_absolute_url(self):
        return reverse("plugins:license_management:licenseassignment", args=[self.pk])