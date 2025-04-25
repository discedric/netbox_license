from django.apps import apps
from netbox.plugins import PluginTemplateExtension

LICENSE_EXPIRY_PROGRESSBAR_TABLE = """
{% with record.get_expiry_progress as wp %}
{% if wp %}
  <div class="progress position-relative" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{{ wp.percent }}">
    <div class="progress-bar bg-{{ wp.color }}" style="width:{{ wp.percent }}%;"></div>
    {% if wp.expired %}
      <span class="position-absolute w-100 h-100 d-flex justify-content-center align-items-center text-white small">
        {{ record.expiry_date|timesince|split:','|first }} ago
      </span>
    {% else %}
      <span class="position-absolute w-100 h-100 d-flex justify-content-center align-items-center text-white small">
        {{ record.expiry_date|timeuntil|split:','|first }} left
      </span>
    {% endif %}
  </div>
{% else %}
<div class="progress position-relative" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="100">
  <div class="progress-bar bg-info" style="width: 100%;">
    <span class="text-white fw-bold">&#8734;</span>
  </div>
</div>
{% endif %}
{% endwith %}
"""


class LicenseProgressBarInjector(PluginTemplateExtension):
    model = 'license_management.license'

    def right_page(self):
        return self.render('license_management/inc/license_progressbar.html', {
            'record': self.context['object']
        })


class DeviceLicenseExtension(PluginTemplateExtension):
    model = "dcim.device"

    def left_page(self):
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

    def left_page(self):
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

    def left_page(self):
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

class LicenseTypeExtension(PluginTemplateExtension):
    model = "license_management.licensetype"

    def right_page(self):
        licenses = self.context['object'].licenses.all()
        license_assignments = sum(l.assignments.count() for l in licenses)
        
        context = {
            "object": self.context["object"],
            "license_assignments": license_assignments,
        }

        return self.render("license_management/inc/licensetype_related.html", extra_context=context)

template_extensions = (
    DeviceLicenseExtension,
    VirtualMachineLicenseExtension,
    ClustersLicenseExtension,
    LicenseProgressBarInjector,
    LicenseTypeExtension,
)
