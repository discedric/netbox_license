from netbox.tables import NetBoxTable
import django_tables2 as tables
from .models import License, LicenseAssignment

class LicenseTable(NetBoxTable):
    """Table for displaying Licenses in NetBox with clickable links."""

    license_key = tables.LinkColumn(
        "plugins:license_management:license",
        args=[tables.A('pk')],
        verbose_name="License Key"
    )
    assigned_count = tables.Column(empty_values=())

    def render_assigned_count(self, record):
        assigned = record.assignments.count()
        max_assignments = record.max_assignments
        return f"{assigned}/{max_assignments}"

    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            "license_key",
            "software_name",
            "manufacturer",
            "assigned_count",
            "assignment_type",
            "expiry_date",
            "purchase_date",
            "status",
        )
        default_columns = fields

class LicenseAssignmentTable(NetBoxTable):
    license = tables.LinkColumn(
        "plugins:license_management:assignment_detail",  # This should match urls.py
        args=[tables.A("pk")],
        verbose_name="License"
    )
    device = tables.Column(verbose_name="Device")
    assigned_quantity = tables.Column(verbose_name="Assigned Quantity")
    assigned_on = tables.DateColumn(verbose_name="Assigned On")
    status = tables.Column(verbose_name="Status")

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = ("pk", "license", "device", "assigned_quantity", "assigned_on", "status")
        default_columns = ("license", "device", "assigned_quantity", "assigned_on", "status")
