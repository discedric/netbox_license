from django.apps import apps
from netbox.plugins import PluginTemplateExtension


LICENSE_EXPIRY_PROGRESSBAR = """
{% load humanize %}
{% with p=record.get_expiry_progress %}
  {% if not p %}
    <span class="text-muted">No expiry date</span>
  {% elif p.days_left < 0 %}
    <!-- Expired -->
    <div class="progress" role="progressbar" style="height:10px;">
      <div class="progress-bar progress-bar-striped text-bg-danger" style="width:100%;">
        Expired {{ p.days_left|abs }} day{{ p.days_left|abs|pluralize }} ago
      </div>
    </div>
  {% else %}
    <!-- Not expired -->
    <div class="progress" role="progressbar" style="height:10px;">
      <div class="progress-bar progress-bar-striped text-bg-success"
           style="width:{{ p.percent }}%;"
           aria-valuenow="{{ p.percent }}"
           aria-valuemin="0"
           aria-valuemax="100">
        {{ p.days_left }} day{{ p.days_left|pluralize }} remaining
      </div>
    </div>
  {% endif %}
{% endwith %}
"""


class DeviceLicenseExtension(PluginTemplateExtension):
    model = "dcim.device"

    def right_page(self):
        object = self.context.get("object")
        LicenseAssignment = apps.get_model("license_management", "LicenseAssignment")
        license_assignments = LicenseAssignment.objects.filter(device=object)

        context = {
            "licenses": license_assignments,
            "object": object,
            "related_object_counts": (
                (
                    "Assigned Licenses",
                    "plugins:license_management:licenseassignment_list",
                    "device_id",
                    object.pk,
                    license_assignments.count()
                ),
            )
        }

        return self.render("license_management/inc/device_info.html", extra_context=context)


class VirtualMachineLicenseExtension(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def right_page(self):
        object = self.context.get("object")
        LicenseAssignment = apps.get_model("license_management", "LicenseAssignment")
        license_assignments = LicenseAssignment.objects.filter(virtual_machine=object)

        context = {
            "licenses": license_assignments,
            "object": object,
            "related_object_counts": (
                (
                    "Assigned Licenses",
                    "plugins:license_management:licenseassignment_list",
                    "virtual_machine_id",
                    object.pk,
                    license_assignments.count()
                ),
            )
        }

        return self.render("license_management/inc/virtual_machines_info.html", extra_context=context)


class ClustersLicenseExtension(PluginTemplateExtension):
    model = "virtualization.cluster"

    def right_page(self):
        object = self.context.get("object")
        LicenseAssignment = apps.get_model("license_management", "LicenseAssignment")
        license_assignments = LicenseAssignment.objects.filter(virtual_machine__cluster=object)

        context = {
            "licenses": license_assignments,
            "object": object,
            "related_object_counts": (
                (
                    "Assigned Licenses",
                    "plugins:license_management:licenseassignment_list",
                    "virtual_machine__cluster_id",
                    object.pk,
                    license_assignments.count()
                ),
            )
        }

        return self.render("license_management/inc/clusters_info.html", extra_context=context)


template_extensions = (
    DeviceLicenseExtension,
    VirtualMachineLicenseExtension,
    ClustersLicenseExtension,
)
