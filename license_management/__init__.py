from netbox.plugins import PluginConfig
from django.urls import include, path
from .version import __version__
from .template_content import template_extensions

class LicenseManagementConfig(PluginConfig):
    name = 'license_management'
    verbose_name = 'License Management'
    version = __version__
    description = 'Inventory License management in NetBox'
    base_url = 'license'
    author = 'Kobe Naessens'
    author_email = 'kobe.naessens@zabun.be'
    min_version = '4.1.0'
    default_settings = {
        'top_level_menu': True,
        'used_status_name': 'used',
        'used_additional_status_names': list(),
        'asset_warranty_expire_warning_days': 90,
    }

    def ready(self):
        self.urlpatterns = [
            path('plugin/license_management/', include('license_management.urls')),
        ]
        super().ready()

config = LicenseManagementConfig