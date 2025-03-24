from netbox.tables import NetBoxTable
import django_tables2 as tables
from django.db.models import Sum
from .models import License, LicenseAssignment


class LicenseTable(NetBoxTable):
    """Table displaying licenses with clickable fields."""

    name = tables.LinkColumn(
        "plugins:license_management:license_detail",
        args=[tables.A('pk')],
        verbose_name="License Name",
        attrs={"a": {"class": "text-primary"}},
    )

    license_key = tables.LinkColumn(
        "plugins:license_management:license_detail",
        args=[tables.A('pk')],
        verbose_name="License Key",
        attrs={"a": {"class": "text-primary"}},
    )

    product_key = tables.Column(verbose_name="Product Key")

    manufacturer = tables.LinkColumn(
        "dcim:manufacturer",
        args=[tables.A("manufacturer.pk")],
        verbose_name="License Manufacturer",
        empty_values=(),
    )

    parent_license = tables.TemplateColumn(
        template_code="""
        {% if record.parent_license %}
            <a href="{% url 'plugins:license_management:license_detail' record.parent_license.pk %}">
                {{ record.parent_license.name }}
            </a>
        {% else %}
            -
        {% endif %}
        """,
        verbose_name="Parent License",
        orderable=False
    )

    assigned_count = tables.Column(empty_values=(), verbose_name="Assigned")
    volume_type = tables.Column(accessor="volume_type", verbose_name="Volume Type")

    def render_assigned_count(self, record):
        assigned = record.assignments.aggregate(total=Sum('volume'))['total'] or 0

        if record.volume_type == "UNLIMITED":
            return f"{assigned}/∞"
        elif record.volume_type == "VOLUME":
            return f"{assigned}/{record.volume_limit or '∞'}"
        return f"{assigned}/1"

    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            "name",
            "license_key",
            "product_key",
            "manufacturer",
            "description",
            "assigned_count",
            "volume_type",
            "parent_license",
            "expiry_date",
            "purchase_date",
        )
        default_columns = fields


class LicenseAssignmentTable(NetBoxTable):
    """Table displaying License Assignments with clickable fields."""

    license_name = tables.TemplateColumn(
        template_code="""
        {% if record.license %}
            <a href="{% url 'plugins:license_management:license_detail' record.license.pk %}">
                {{ record.license.name }}
            </a>
        {% else %}
            -
        {% endif %}
        """,
        verbose_name="License Name",
        orderable=False
    )

    license_key = tables.TemplateColumn(
        template_code="""
        {% if record.license %}
            <a href="{% url 'plugins:license_management:license_detail' record.license.pk %}">
                {{ record.license.license_key }}
            </a>
        {% else %}
            -
        {% endif %}
        """,
        verbose_name="License Key",
        orderable=False
    )

    manufacturer = tables.LinkColumn(
        "dcim:manufacturer",
        args=[tables.A("license.manufacturer.pk")],
        verbose_name="License Manufacturer",
        empty_values=(),
    )

    device = tables.LinkColumn(
        "dcim:device",
        args=[tables.A("device.pk")],
        verbose_name="Device"
    )

    device_manufacturer = tables.TemplateColumn(
        template_code="""
        {% if record.device.device_type.manufacturer %}
            <a href="{% url 'dcim:manufacturer' record.device.device_type.manufacturer.pk %}">
                {{ record.device.device_type.manufacturer.name }}
            </a>
        {% else %}
            -
        {% endif %}
        """,
        verbose_name="Device Manufacturer",
        orderable=False
    )

    virtual_machine = tables.TemplateColumn(
        template_code="""
        {% if record.virtual_machine %}
            <a href="{% url 'virtualization:virtualmachine' record.virtual_machine.pk %}">
                {{ record.virtual_machine.name }}
            </a>
        {% else %}
            -
        {% endif %}
        """,
        verbose_name="Virtual Machine",
        orderable=False
    )

    volume = tables.Column(verbose_name="Volume")
    assigned_to = tables.DateColumn(verbose_name="Assigned On")
    description = tables.Column(verbose_name="Description", empty_values=())

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = (
            "license_name",
            "license_key",
            "manufacturer",
            "device",
            "device_manufacturer",
            "virtual_machine",
            "volume",
            "assigned_to",
            "description"
        )
        default_columns = fields
