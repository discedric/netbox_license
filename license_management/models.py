from django.db import models

class SoftwareLicense(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=100)
    license_key = models.CharField(max_length=255)
    expiration_date = models.DateField()
    purchased_on = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
