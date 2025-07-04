from netbox.plugins import PluginConfig
from django.urls import include, path
from .version import __version__
from .template_content import template_extensions

class NetboxLicenseConfig(PluginConfig):
    name = 'netbox_license'
    verbose_name = 'NetBox License'
    version = __version__
    description = 'License management Plugin for NetBox'
    base_url = 'license'
    author = 'Kobe Naessens'
    author_email = 'kobe.naessens@zabun.be'
    min_version = '4.3.0'
    default_settings = {
        'top_level_menu': True,
    }

    def ready(self):
        super().ready()
        from . import  events
        from . import jobs

config = NetboxLicenseConfig