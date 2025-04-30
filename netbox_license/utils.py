from django.apps import apps
from django.db.models import Q

def query_assigned_licenses(device):
    """
    Retrieves a queryset of licenses assigned to a given device.

    Args:
        device (Device): The device for which to fetch assigned licenses.

    Returns:
        QuerySet: A queryset containing licenses assigned to the device.
    """
    License = apps.get_model('netbox_license', 'License')
    return License.objects.filter(assignments__device=device)

def get_license_names_for_device(device):
    """
    Returns a list of license names assigned to a specific device.

    Args:
        device (Device): The device object.

    Returns:
        list: A list of license names assigned to the device.
    """
    return list(query_assigned_licenses(device).values_list('name', flat=True))
