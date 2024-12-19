from netbox.plugins import PluginConfig
from .version import __version__

class LicenceManagerConfig(PluginConfig):
    name = 'license_management'
    verbose_name = 'License Management'
    version = __version__
    description = 'Inventory License management in NetBox'
    author = 'Cedric Vaneessen'
    author_email = 'cedric.vaneessen@zabun.be'
    base_url = 'Licenses'
    min_version = '4.1.0'

    def ready(self):
        super().ready()

config = LicenceManagerConfig