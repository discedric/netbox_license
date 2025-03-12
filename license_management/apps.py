# license_management/apps.py
# from django.apps import AppConfig
from extras.plugins import PluginConfig

class LicenseManagementConfig(PluginConfig):
    name = 'license_management'
    verbose_name = 'License Management'
    base_url = "license_management"