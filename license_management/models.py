from django.db import models
from netbox.models import NetBoxModel  # NetBox base model
from dcim.models import Manufacturer, Device  # Import NetBox Manufacturer & Device models
from django.utils.timezone import now
from django.urls import reverse
from django.core.exceptions import ValidationError

class License(NetBoxModel):
    """Represents a software license that can be assigned to devices, cores, or users."""

    ASSIGNMENT_TYPE_CHOICES = [
        ('DEVICES', 'Devices'),
        ('CORES', 'CPU Cores'),
        ('USERS', 'Users'),
    ]

    license_key = models.CharField(max_length=255, unique=True)
    software_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="licenses",
        null=True, 
        blank=True  
    )
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    max_assignments = models.IntegerField(default=1)
    assignment_type = models.CharField(
        max_length=50, choices=ASSIGNMENT_TYPE_CHOICES, default='DEVICES'
    )
    type = models.CharField(
        max_length=50,
        choices=[
            ('PERPETUAL', 'Perpetual'),
            ('SUBSCRIPTION', 'Subscription'),
            ('TRIAL', 'Trial'),
            ('OPEN_SOURCE', 'Open Source'),
            ('ENTERPRISE', 'Enterprise'),
        ],
        default='SUBSCRIPTION',
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('ACTIVE', 'Active'),
            ('EXPIRED', 'Expired'),
            ('REVOKED', 'Revoked'),
        ],
        default='ACTIVE',
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.license_key} - {self.software_name} ({self.get_type_display()}, {self.max_assignments} {self.get_assignment_type_display()})"

    def get_absolute_url(self):
        if self.pk:
            return reverse("plugins:license_management:license_detail", args=[self.pk])
        return "#"


class LicenseAssignment(NetBoxModel):
    """Represents an assignment of a License to a Device (or other types of entities)."""

    license = models.ForeignKey(
        License, on_delete=models.CASCADE, related_name="assignments"
    )
    assigned_quantity = models.IntegerField(default=1)
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="license_assignments",
        null=True,
        blank=True
    )
    assigned_on = models.DateTimeField(default=now)
    status = models.CharField(
        max_length=50,
        choices=[
            ('ASSIGNED', 'Assigned'),
            ('REVOKED', 'Revoked'),
            ('EXPIRED', 'Expired'),
        ],
        default='ASSIGNED',
    )

    def clean(self):
        """Ensure assignments match the license type constraints."""
        if self.license.assignment_type == "DEVICES":
            if not self.device:
                raise ValidationError("Device is required for device-based licenses.")
        elif self.license.assignment_type in ["CORES", "USERS"]:
            if self.assigned_quantity <= 0:
                raise ValidationError("Assigned quantity must be greater than 0 for core/user-based licenses.")

    def get_absolute_url(self):
        """Ensure NetBox correctly resolves the assignment detail URL."""
        return reverse("plugins:license_management:assignment_detail", args=[self.pk])

    def __str__(self):
        """Better string representation for admin panel & NetBox UI."""
        if self.license.assignment_type == "DEVICES":
            return f"{self.device.name} - {self.license.license_key} [{self.get_status_display()}]"
        return f"{self.license.license_key} [{self.get_status_display()}] - {self.assigned_quantity} {self.license.get_assignment_type_display()}"
