from extras.jobs import Job
from netbox_license.models.license import License
from netbox_license.notifications import send_slack_notification

class LicenseStatusCheckJob(Job):
    name = "License Status Checker"

    def run(self):
        for license in License.objects.all():
            old_status = license.status
            new_status = license.compute_status()

            if old_status != new_status:
                license.status = new_status
                license.save()
                send_slack_notification(license, old_status, new_status)
