from django.db.models import Sum
from django_tables2 import tables, TemplateColumn
from netbox.tables import NetBoxTable
from .models import License, LicenseAssignment, LicenseType
from .template_content import LICENSE_EXPIRY_PROGRESSBAR_TABLE

# ---------- LicenseType ----------

class LicenseTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    slug = tables.Column()
    manufacturer = tables.Column(
        verbose_name="Manufacturer",
        linkify=True
    )
    instances = tables.Column(
        verbose_name="Instances",
        accessor="license_count",
        order_by="license_count",
    )
    product_code = tables.Column(verbose_name="Product Code")
    ean_code = tables.Column(verbose_name="EAN Code")
    volume_type = tables.Column(verbose_name="Volume Type")
    license_model = tables.Column(verbose_name="License Model")
    purchase_model = tables.Column(verbose_name="Purchase Model")
    description = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = LicenseType
        fields = (
            "id", "name", "slug", "manufacturer",
            "product_code", "ean_code",
            "volume_type", "license_model", "purchase_model",
            "description"
        )
        default_columns = (
        "name", "manufacturer",
        "product_code", "volume_type",
        "license_model", "instances",
    )

# ---------- License ----------

class LicenseTable(NetBoxTable):
    license_type = tables.Column(
        accessor="license_type.name",
        linkify=lambda record: record.license_type.get_absolute_url(),
        verbose_name="License Type"
    )
    license_key = tables.Column(linkify=True)
    product_key = tables.Column(verbose_name="Product Key")
    serial_number = tables.Column(verbose_name="Serial Number")
    manufacturer = tables.Column(
        verbose_name="License Manufacturer",
        accessor="manufacturer",
        linkify=True
    )
    parent_license = tables.Column(
        accessor="parent_license",
        verbose_name="Parent License",
        linkify=True
    )
    parent_license_type = tables.Column(
        verbose_name="Parent License Type",
        accessor="parent_license.license_type.name",
        linkify=True,
        order_by="parent_license__license_type__name"
    )

    volume_type = tables.Column(verbose_name="Volume Type", empty_values=())
    is_parent_license = tables.Column(verbose_name='Parent', empty_values=())
    is_child_license = tables.Column(verbose_name='Child', empty_values=())
    assigned_count = tables.Column(empty_values=(), verbose_name="Assigned")

    expiry_bar = TemplateColumn(
        template_code=LICENSE_EXPIRY_PROGRESSBAR_TABLE,
        verbose_name="Expirty status",
        order_by="expiry_date",
    )


    def render_assigned_count(self, record):
        assigned = record.assignments.aggregate(total=Sum('volume'))['total'] or 0
        volume_type = getattr(record.license_type, 'volume_type', None)

        if volume_type == "UNLIMITED":
            return f"{assigned}/∞"
        elif volume_type == "VOLUME":
            return f"{assigned}/{record.volume_limit or '∞'}"
        return f"{assigned}/1"

    def render_volume_type(self, record):
        return getattr(record.license_type, 'get_volume_type_display', lambda: '—')()

    def render_is_parent_license(self, record):
        return "✅" if record.is_parent_license else "❌"

    def render_is_child_license(self, record):
        return "✅" if record.is_child_license else "❌"

    
    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            "license_type", "license_key", "product_key", "serial_number",
            "manufacturer", "parent_license", "parent_license_type",
            "is_parent_license", "is_child_license", "description",
            "assigned_count", "volume_type",
            "expiry_date", "purchase_date", "expiry_bar",
        )
        default_columns = (
        "license_key", "license_type", "manufacturer", "assigned_count",
        "parent_license", "serial_number", "volume_type"
    )

# ---------- Assignments ----------

class LicenseAssignmentTable(NetBoxTable):
    license = tables.Column(
        accessor="license",
        verbose_name="License",
        linkify=True
    )
    license_key = tables.Column(
        accessor="license.license_key",
        verbose_name="License Key",
        linkify=True
    )
    license_type = tables.Column(
        accessor='license.license_type',
        verbose_name='License Type',
        linkify=True,
        order_by='license__license_type__name'
    )
    manufacturer = tables.Column(
        accessor="license.manufacturer",
        verbose_name="License Manufacturer",
        linkify=True
    )
    device = tables.Column(
        accessor="device",
        verbose_name="Device",
        linkify=True
    )
    device_manufacturer = tables.Column(
        accessor="device.device_type.manufacturer",
        verbose_name="Device Manufacturer",
        linkify=True
    )
    virtual_machine = tables.Column(
        accessor="virtual_machine",
        verbose_name="Virtual Machine",
        linkify=True
    )
    volume = tables.Column(verbose_name="Volume")
    assigned_on = tables.Column(verbose_name="Assigned On")
    description = tables.Column(verbose_name="Description")

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = (
            "license", "license_key", "manufacturer",
            "device", "device_manufacturer",
            "virtual_machine", "volume",
            "assigned_on", "description"
        )
        default_columns = (
            "license", "license_type",
            "device", "virtual_machine",
            "volume",
        )
        
