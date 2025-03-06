from django.db import models
from netbox.models import NetBoxModel  # NetBox base model
from dcim.models import Manufacturer, Device  # Import NetBox Manufacturer & Device models
from django.utils.timezone import now

class License(NetBoxModel):
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


class LicenseAssignment(NetBoxModel):
    license = models.ForeignKey(
        License, on_delete=models.CASCADE, related_name="assignments"
    )
    assigned_quantity = models.IntegerField(default=1)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="license_assignments", null=True, blank=True)
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
    description = models.TextField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.device.name} - {self.license.license_key} [{self.get_status_display()}] - {self.assigned_quantity} {self.license.get_assignment_type_display()}"
