from netbox.search import SearchIndex, register_search
from .models import License, LicenseAssignment, LicenseType

@register_search
class LicenseTypeIndex(SearchIndex):
    model = LicenseType
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs =('base_license','product_code', 'volume_type', 'license_model')
    
@register_search
class LicenseIndex(SearchIndex):
    model = License
    fields = (
        ('license_key', 100),
        ('serial_number',100),
        ('comments', 5000),
    )
    display_attrs =('license_type',)
    ## In case you only have one attribute, away put a ',' at the end!

@register_search
class LicenseAssignmentIndex(SearchIndex):
    model = LicenseAssignment
    fields = (
        ('license', 100),
        ('device', 100),
        ('virtual_machine', 500),
        ('comments', 5000),
    )
    display_attrs = ('volume', 'assigned_on')

