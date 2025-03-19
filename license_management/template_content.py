from django.template import Template
from netbox.plugins import PluginTemplateExtension
from django.apps import apps

LICENSE_TEMPLATE = """
{% if licenses %}
  <div class="panel panel-default">
    <div class="panel-heading">
      <strong>Assigned Licenses</strong>
    </div>
    <div class="panel-body">
      <ul>
        {% for license_name in licenses %}
          <li>{{ license_name }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
{% endif %}
"""

class DeviceLicenseExtension(PluginTemplateExtension):
    """
    Extends the device detail view to include assigned licenses.
    """
    model = "dcim.device" 

    def right_page(self):
        object = self.context.get("object")

        LicenseAssignment = apps.get_model("license_management", "LicenseAssignment")

        license_assignments = LicenseAssignment.objects.filter(device=object)
        licenses = license_assignments.values_list("license__name", flat=True)

        context = {"licenses": licenses}
        license_template = Template(LICENSE_TEMPLATE)
        return license_template.render(self.context)

template_extensions = (DeviceLicenseExtension,)
