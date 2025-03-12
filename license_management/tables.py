from netbox.tables import NetBoxTable
import django_tables2 as tables
from .models import License, LicenseAssignment

class LicenseTable(NetBoxTable):
    """Table for displaying Licenses in NetBox with clickable links."""

    license_key = tables.LinkColumn(
    "plugins:license_management:license_detail",  # Corrected name
    args=[tables.A("pk")],
    verbose_name="License Key"
)

    software_name = tables.LinkColumn(
    "plugins:license_management:license_detail",  # Ensure it links correctly
    args=[tables.A("pk")],
    verbose_name="Software Name"
)

    manufacturer = tables.Column(verbose_name="Manufacturer")
    max_assignments = tables.Column(verbose_name="Max Assignments")
    assignment_type = tables.Column(verbose_name="Assignment Type")
    expiry_date = tables.DateColumn(verbose_name="Expiry Date", format="Y-m-d")
    purchase_date = tables.DateColumn(verbose_name="Purchase Date", format="Y-m-d")
    status = tables.Column(verbose_name="Status")

    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            "license_key",
            "software_name",
            "manufacturer",
            "max_assignments",
            "assignment_type",
            "expiry_date",
            "purchase_date",
            "status",
        )
        default_columns = fields


class LicenseAssignmentTable(NetBoxTable):
    """Table for displaying License Assignments."""
    
    license = tables.LinkColumn(
        "plugins:license_management:license_detail",  # Corrected URL name
        args=[tables.A("license.pk")],
        verbose_name="License"
    )

    device = tables.LinkColumn(
        "dcim:device",
        args=[tables.A("device.pk")],
        verbose_name="Device"
    )

    assigned_quantity = tables.Column(verbose_name="Assigned Quantity")
    assigned_on = tables.DateColumn(verbose_name="Assigned On")
    status = tables.Column(verbose_name="Status")

    class Meta:
        model = LicenseAssignment
        fields = ("license", "device", "assigned_quantity", "assigned_on", "status")
