from django.utils.translation import gettext as _
from netbox.events import EventType, EVENT_TYPE_KIND_WARNING

EventType(
    name='netbox_license.expirystatus',
    text=_('License Status'),
    kind=EVENT_TYPE_KIND_WARNING,
).register()
