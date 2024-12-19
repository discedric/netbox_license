from extras.plugins import PluginConfig
from django.urls import path
from . import views

class PluginConfig(PluginConfig):
    name = 'license_management'
    verbose_name = 'Software License Management'
    description = 'A plugin to manage software licenses'
    version = '0.1.0'
    author = 'Cedric Vaneessen'

    def ready(self):
        # Import views to register URLs
        from . import views
        pass

# Optional: Add URL routing if your plugin has views
urlpatterns = [
    path('licenses/', views.list_licenses, name='list_licenses'),
]
