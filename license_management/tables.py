from django.db.models import Sum
from django_tables2 import tables, TemplateColumn
from netbox.tables import NetBoxTable
from django.urls import reverse
from django.utils.html import format_html
from .models import License, LicenseAssignment, LicenseType
from .template_content import LICENSE_EXPIRY_PROGRESSBAR_TABLE

# ---------- LicenseType ----------

class LicenseTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    slug = tables.Column()
    manufacturer = tables.Column(verbose_name="Manufacturer", linkify=True)

    instances = tables.Column(
        verbose_name="Instances",
        accessor="license_count",
        order_by="license_count",
        empty_values=(),
    )

    def render_instances(self, value, record):
        url = reverse('plugins:license_management:license_list') + f'?license_type_id={record.pk}'
        return format_html('<a href="{}">{}</a>', url, value)

    product_code = tables.Column(verbose_name="Product Code")
    ean_code = tables.Column(verbose_name="EAN Code")
    volume_type = tables.Column(verbose_name="Volume Type")
    volume_relation = tables.Column(verbose_name="Volume Relation")
    license_model = tables.Column(verbose_name="License Model")
    purchase_model = tables.Column(verbose_name="Purchase Model")
    description = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = LicenseType
        fields = (
            "id", "name", "slug", "manufacturer",
            "product_code", "ean_code",
            "volume_type", "volume_relation", "license_model", "purchase_model",
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
    license_model = tables.Column(
        accessor='license_type.license_model',
        verbose_name='License Model',
        order_by='license_type__license_model'
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

    volume_type = tables.Column(
        accessor="license_type.get_volume_type_display",
        verbose_name="Volume Type",
        order_by="license_type__volume_type"
    )

    volume_relation = tables.Column(
        accessor="license_type.volume_relation",
        verbose_name="Volume Relation",
        order_by="license_type__volume_relation"
    )
    is_parent_license = tables.Column(
        verbose_name='Parent',
        accessor='is_parent_license_value',
        order_by='is_parent_license_value'
    )

    is_child_license = tables.Column(
        verbose_name='Child',
        accessor='is_child_license_value',
        order_by='is_child_license_value'
    )

    assigned_count = tables.Column(
        verbose_name='Assigned',
        accessor='assigned_count_value',
        order_by='assigned_count_value'
    )

    expiry_bar = TemplateColumn(
        template_code=LICENSE_EXPIRY_PROGRESSBAR_TABLE,
        verbose_name="Expirty status",
        order_by="expiry_date",
    )

    
    def render_volume_type(self, record):
        return getattr(record.license_type, 'get_volume_type_display', lambda: '—')()

    def render_is_parent_license(self, record):
        return "✅" if getattr(record, 'is_parent_license_value', False) else "❌"

    def render_is_child_license(self, record):
        return "✅" if getattr(record, 'is_child_license_value', False) else "❌"
    
    def render_assigned_count(self, record):
        assigned = getattr(record, 'assigned_count_value', 0) or 0
        volume_type = getattr(record.license_type, 'volume_type', None)
        volume_limit = record.volume_limit

        if volume_type == "unlimited":
            max_str = "∞"
        elif volume_type == "volume":
            max_str = volume_limit if volume_limit is not None else "∞"
        else:
            max_str = 1

        url = reverse('plugins:license_management:licenseassignment_list') + f'?license={record.pk}'
        return format_html(f'<a href="{url}">{assigned}/{max_str}</a>')

    
    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            "license_type", "license_model", "license_key", "product_key", "serial_number",
            "manufacturer", "parent_license", "parent_license_type",
            "is_parent_license", "is_child_license", "description",
            "assigned_count", "volume_type", "volume_relation",
            "expiry_date", "purchase_date", "expiry_bar",
        )
        default_columns = (
        "license_key", "license_type", "manufacturer", "assigned_count",
        "parent_license", "serial_number", "volume_type"
    )

# ---------- Assignments ----------

class LicenseAssignmentTable(NetBoxTable):
    
    license_key = tables.Column(
        accessor="license",
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

    volume_relation = tables.Column(
        accessor="license.license_type.volume_relation",
        verbose_name="Volume Relation",
        order_by="license__license_type__volume_relation"
    )
    assigned_to = tables.Column(verbose_name="Assigned On")
    description = tables.Column(verbose_name="Description")

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = (
            "license_key", "license_type", "manufacturer",
            "device", "device_manufacturer",
            "virtual_machine", "volume", "volume_relation",
            "assigned_to", "description"
        )
        default_columns = (
            "license", "device", "virtual_machine", "volume",
        )
        
