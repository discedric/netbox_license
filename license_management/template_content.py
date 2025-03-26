from django.apps import apps
from netbox.plugins import PluginTemplateExtension

class ManufacturerLicenseExtension(PluginTemplateExtension):
    model = "dcim.manufacturer"

    def right_page(self):
        object = self.context.get("object")
        LicenseAssignment = apps.get_model("license_management", "LicenseAssignment")
        license_assignments = LicenseAssignment.objects.filter(manufacturer=object)

        context = {
            "licenses": license_assignments,
            "object": object
        }
        return self.render("license_management/inc/manufacturers_info.html", extra_context=context)

class DeviceLicenseExtension(PluginTemplateExtension):
    model = "dcim.device"

    def right_page(self):
        object = self.context.get("object")
        LicenseAssignment = apps.get_model("license_management", "LicenseAssignment")
        license_assignments = LicenseAssignment.objects.filter(device=object)
        context = {
            "licenses": license_assignments,
            "object": object
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
            "object": object 
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
            "object": object 
        }
        return self.render("license_management/inc/clusters_info.html", extra_context=context)

template_extensions = (
    ManufacturerLicenseExtension,
    DeviceLicenseExtension,
    VirtualMachineLicenseExtension,
    ClustersLicenseExtension,
)