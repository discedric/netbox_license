from django.db import models
from netbox.models import NetBoxModel  # Ensure you use NetBox's base model

class License(NetBoxModel):
    ASSIGNMENT_TYPE_CHOICES = [
        ('DEVICES', 'Devices'),
        ('CORES', 'CPU Cores'),
        ('USERS', 'Users'),
    ]

    license_key = models.CharField(max_length=255, unique=True)
    software_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    vendor = models.CharField(max_length=255)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    max_assignments = models.IntegerField(default=1)  # Number of devices/cores/users allowed
    assignment_type = models.CharField(max_length=50, choices=ASSIGNMENT_TYPE_CHOICES, default='DEVICES')  # NEW FIELD
    type = models.CharField(max_length=50, choices=[
        ('PERPETUAL', 'Perpetual'),
        ('SUBSCRIPTION', 'Subscription'),
        ('TRIAL', 'Trial'),
        ('OPEN_SOURCE', 'Open Source'),
        ('ENTERPRISE', 'Enterprise'),
    ], default='SUBSCRIPTION')
    status = models.CharField(max_length=50, choices=[
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('REVOKED', 'Revoked'),
    ], default='ACTIVE')
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.license_key} - {self.software_name} ({self.get_type_display()}, {self.max_assignments} {self.get_assignment_type_display()})"


class LicenseAssignment(NetBoxModel):
    license = models.ForeignKey(License, on_delete=models.CASCADE, related_name="assignments")
    assigned_quantity = models.IntegerField(default=1)  # NEW FIELD (how many cores/devices/users assigned)
    device_name = models.CharField(max_length=255, blank=True, null=True)  # Optional for core-based licensing
    device_owner = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=50, choices=[
        ('PC', 'PC'),
        ('SERVER', 'Server'),
        ('MOBILE', 'Mobile'),
        ('CLOUD', 'Cloud Instance'),
        ('OTHER', 'Other'),
    ], default='PC')
    status = models.CharField(max_length=50, choices=[
        ('ASSIGNED', 'Assigned'),
        ('REVOKED', 'Revoked'),
        ('EXPIRED', 'Expired'),
    ], default='ASSIGNED')
    description = models.TextField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    activation_date = models.DateField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.device_name or 'N/A'} ({self.serial_number or 'N/A'}) - {self.license.license_key} [{self.get_status_display()}] - {self.assigned_quantity} {self.license.get_assignment_type_display()}"

