from netbox.plugins import PluginConfig
from django.urls import include, path
from .version import __version__

class LicenceManagerConfig(PluginConfig):
    name = 'license_management'
    verbose_name = 'License Management'
    version = __version__
    description = 'Inventory License management in NetBox'
    author = 'Cedric Vaneessen'
    author_email = 'cedric.vaneessen@zabun.be'
    min_version = '4.1.0'
    default_settings = {
        'top_level_menu': True,
        'used_status_name': 'used',
        'used_additional_status_names': list(),
        'asset_warranty_expire_warning_days': 90,
    }

    def ready(self):
        self.urlpatterns = [
            path('plugins/license_management', include('license_management.urls'))
        ]
        super().ready()

config = LicenceManagerConfig