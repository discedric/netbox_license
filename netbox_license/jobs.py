from netbox.jobs import JobRunner, system_job
from core.choices import JobIntervalChoices
from netbox_license.models.license import License

@system_job(interval=JobIntervalChoices.INTERVAL_DAILY) 
class LicenseStatusCheckJob(JobRunner):
    class Meta:
        name = "License Status Checker"

    def run(self, *args, **kwargs):
        for license in License.objects.all():
            new_status = license.compute_status()
            if license.status != new_status:
                license.status = new_status
                license.save()
