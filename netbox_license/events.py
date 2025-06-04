# from django.utils.translation import gettext_lazy as _  # :white_check_mark: for i18n support
from django.utils.translation import gettext as _
from netbox.registry import registry
from netbox.events import EventType, EVENT_TYPE_KIND_WARNING, EVENT_TYPE_KIND_DANGER

EventType(
    name='netbox_license.expirystatus',
    text=_('License Status'),
    kind=EVENT_TYPE_KIND_WARNING
).register()