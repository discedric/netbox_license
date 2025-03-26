from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine
from django.utils.timezone import now
from django.urls import reverse
from django.core.exceptions import ValidationError


class License(NetBoxModel):
    """Represents a software license that can be assigned to devices."""

    VOLUME_TYPE_CHOICES = [
        ("SINGLE", "Single License (1 device)"),
        ("VOLUME", "Volume License (multiple devices)"),
        ("UNLIMITED", "Unlimited License"),
    ]
    
    name = models.CharField(max_length=255)
    license_key = models.CharField(max_length=255, unique=True)
    product_key = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="licenses",
        null=True,
        blank=True
    )
    purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    volume_type = models.CharField(  
        max_length=20, choices=VOLUME_TYPE_CHOICES, default="SINGLE"
    )
    volume_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Maximum number of assignments allowed. Required if volume license."
    )
    parent_license = models.ForeignKey(
        to='self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_licenses",
        help_text="Link to parent license for extensions."
    )

    clone_fields = [
        'name', 'license_key', 'product_key', 'serial_number', 'description',
    ]

    def clean(self):
        if self.volume_type == "SINGLE":
            self.volume_limit = 1
        elif self.volume_type == "UNLIMITED":
            self.volume_limit = None
        elif self.volume_type == "VOLUME":
            if not self.volume_limit or self.volume_limit < 2:
                raise ValidationError("Volume licenses require a volume limit of at least 2.")

    def current_usage(self):
        assigned = self.assignments.aggregate(models.Sum('volume'))['volume__sum'] or 0
        return assigned

    def usage_display(self):
        if self.volume_type == "UNLIMITED":
            return f"{self.current_usage()}/∞"
        return f"{self.current_usage()}/{self.volume_limit}"

    @property
    def is_parent_license(self):
        return self.sub_licenses.exists()

    @property
    def is_child_license(self):
        return self.parent_license is not None

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:license_management:license", args=[self.pk])

    class Meta:
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'



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

        license = getattr(self, 'license', None)
        manufacturer = getattr(self, 'manufacturer', None)

        if license and manufacturer and license.manufacturer != manufacturer:
            raise ValidationError("Selected license does not belong to the chosen manufacturer.")

        if license:
            self.manufacturer = license.manufacturer

        if self.device and not self.device_manufacturer:
            self.device_manufacturer = self.device.device_type.manufacturer

        if license:
            volume_type = license.volume_type
            if volume_type == "SINGLE":
                self.volume = 1
                existing_assignments = license.assignments.exclude(pk=self.pk).count()
                if existing_assignments >= 1:
                    raise ValidationError("Single licenses can only be assigned to one entity (Device or VM).")

            elif volume_type == "VOLUME":
                if self.volume < 1:
                    raise ValidationError("Volume quantity must be at least 1.")
                total_assigned_volume = (
                    license.assignments.exclude(pk=self.pk)
                    .aggregate(models.Sum('volume'))['volume__sum'] or 0
                )
                if total_assigned_volume + self.volume > license.volume_limit:
                    raise ValidationError(
                        f"Exceeds volume limit ({license.volume_limit}). Currently assigned: {total_assigned_volume}."
                    )

    def __str__(self):
        return f"{self.license.name} → {self.device or self.virtual_machine} ({self.volume})"

    def get_absolute_url(self):
        return reverse("plugins:license_management:licenseassignment", args=[self.pk])
