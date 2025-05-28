from django.db import models
from netbox.models import NetBoxModel
from django.utils.timezone import now
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from netbox_license.models.licensetype import LicenseType
from taggit.managers import TaggableManager
from ..choices import AssignmentKindChoices

class License(NetBoxModel):
    license_key = models.CharField(max_length=255, unique=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    license_type = models.ForeignKey(
        'LicenseType',
        on_delete=models.PROTECT,
        related_name="licenses"
    )

    purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    volume_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Required if license type is volume."
    )
    parent_license = models.ForeignKey(
        to='self',
        null=True, blank=True,
        on_delete=models.PROTECT,
        related_name="sub_licenses",
        help_text="Link to parent license for extensions."
    )
    tags = TaggableManager(related_name="lm_license_tags")

    def clean(self):
        if self.license_type_id:
            try:
                license_type = self.license_type
                self.manufacturer = license_type.manufacturer
            except LicenseType.DoesNotExist:
                pass

        if self.pk:
            original = License.objects.get(pk=self.pk)
            if original.license_type != self.license_type:
                raise ValidationError({
                    "license_type": "Changing the license type of an existing license is not allowed."
                })

        vt = self.license_type.volume_type if self.license_type_id and self.license_type else None

        if vt == "single":
            if self.volume_limit and self.volume_limit != 1:
                raise ValidationError({"volume_limit": "Single licenses must have a volume limit of exactly 1."})
            self.volume_limit = 1

        elif vt == "unlimited":
            self.volume_limit = None

        elif vt == "volume":
            if not self.volume_limit or self.volume_limit < 2:
                raise ValidationError("Volume licenses require a volume limit of at least 2.")

        if self.purchase_date and self.expiry_date:
            if self.expiry_date < self.purchase_date:
                raise ValidationError(_("Expiry date cannot be earlier than purchase date."))

    def current_usage(self):
        assigned = self.assignments.aggregate(models.Sum('volume'))['volume__sum'] or 0
        return assigned

    def usage_display(self):
        vt = self.license_type.volume_type if self.license_type else ""
        if vt == "unlimited":
            return f"{self.current_usage()}/∞"
        return f"{self.current_usage()}/{self.volume_limit}"
    
    

    @property
    def is_parent_license(self):
        return self.sub_licenses.exists()

    @property
    def is_child_license(self):
        return self.parent_license is not None
    
    @property
    def usage_kinds(self):
        kinds = set(a.kind for a in self.assignments.all())
        return [dict(AssignmentKindChoices).get(k) for k in kinds if k]

    def __str__(self):
        return f"{self.license_key}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_license:license", args=[self.pk])

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"

    @property
    def get_expiry_progress(self):
        today = date.today()

        if self.expiry_date:
            days_left = (self.expiry_date - today).days
            
            if days_left < 0:
                color = "danger"
            elif days_left < 90:
                color = "warning"
            else:
                color = "success"

            if self.purchase_date:
                total_days = (self.expiry_date - self.purchase_date).days
                if total_days > 0:
                    percent = int(100 * (1 - (days_left / total_days)))
                    if percent < 10 and days_left > 0:
                        percent = 10
                else:
                    percent = 100
            else:
                percent = 100  

            return {
                "percent": max(0, min(percent, 100)),
                "days_left": days_left,
                "color": color,
                "expired": days_left < 0,
            }

        return None

    @property
    def expiry_elapsed(self):
        return date.today() - self.purchase_date if self.purchase_date else None

    @property
    def expiry_remaining(self):
        if self.expiry_date:
            return self.expiry_date - date.today()
        return None

    @property
    def expiry_total(self):
        if self.purchase_date and self.expiry_date:
            return self.expiry_date - self.purchase_date
        return None

    @property
    def expiry_progress(self):
        if not self.expiry_date:
            return None
        if not self.purchase_date:
            days_left = (self.expiry_date - date.today()).days
            return 10 if days_left > 0 else 100
        try:
            percent = int(100 * (self.expiry_elapsed / self.expiry_total))
            if percent < 10 and self.expiry_remaining.days > 0:
                percent = 10
            return max(0, min(percent, 100))
        except ZeroDivisionError:
            return 100
    
    class Meta:
        verbose_name = "Licenses"
        verbose_name_plural = "Licenses"