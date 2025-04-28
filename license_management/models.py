from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine
from django.utils.timezone import now
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from taggit.managers import TaggableManager
from .choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
    VolumeRelationChoices,
    LicenseStatusChoices,
    LicenseAssignmentStatusChoices
)


# ---------- LicenseType ----------

class LicenseType(NetBoxModel):
    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)
    
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="license_types"
    )

    product_code = models.CharField(max_length=255, blank=True, null=True)

    ean_code = models.CharField(
    "EAN code",
    max_length=255,
    blank=True,
    null=True
)

    volume_type = models.CharField(
        max_length=20, 
        choices=VolumeTypeChoices
    )

    volume_relation = models.CharField(
        max_length=20,
        choices=VolumeRelationChoices,
        blank=True,
        null=True,
        help_text="What the license volume applies to (e.g., Users, Cores, etc.)."
    )

    license_model = models.CharField(
        max_length=20,
        choices=LicenseModelChoices,
        default="base"
    )
    base_license = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expansions",
        help_text="Only for expansion licenses. Must reference a base license."
    )
    purchase_model = models.CharField(max_length=20, choices=PurchaseModelChoices, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    clone_fields = ['manufacturer', 'volume_type', 'license_model', 'purchase_model']

    def clean(self):
        super().clean()

        if self.license_model == LicenseModelChoices.EXPANSION:
            if not self.base_license:
                raise ValidationError({
                    "base_license": "An Expansion license type must reference a Base license."
                })
            if self.base_license.license_model != LicenseModelChoices.BASE:
                raise ValidationError({
                    "base_license": "Base License must be of type 'base'."
                })

        elif self.license_model == LicenseModelChoices.BASE:
            if self.base_license is not None:
                raise ValidationError({
                    "base_license": "Only Expansion licenses can reference a base license."
                })

        if self.pk:
            original = LicenseType.objects.get(pk=self.pk)
            has_licenses = self.licenses.exists()

            if has_licenses:
                if original.license_model != self.license_model:
                    raise ValidationError({
                        "license_model": "Cannot change license model: there are existing licenses linked to this license type."
                    })

                if original.volume_type != self.volume_type:
                    raise ValidationError({
                        "volume_type": "Cannot change volume type: there are existing licenses linked to this license type."
                    })

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:license_management:licensetype", args=[self.pk])

    class Meta:
        verbose_name = "License Type"
        verbose_name_plural = "License Types"

# ---------- License ----------

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

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="lm_licenses",
        null=True, blank=True,
        help_text="Redundant for filtering; copied from license_type."
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
        on_delete=models.SET_NULL,
        related_name="sub_licenses",
        help_text="Link to parent license for extensions."
    )
    tags = TaggableManager(related_name="lm_license_tags")

    def clean(self):
        if self.license_type:
            self.manufacturer = self.license_type.manufacturer

        if self.pk:
            original = License.objects.get(pk=self.pk)
            if original.license_type != self.license_type:
                raise ValidationError({
                    "license_type": "Changing the license type of an existing license is not allowed."
                })

        vt = self.license_type.volume_type if self.license_type else None

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

    def __str__(self):
        return f"{self.license_key}"

    def get_absolute_url(self):
        return reverse("plugins:license_management:license", args=[self.pk])

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"

    @property
    def get_expiry_progress(self):
        today = date.today()

        if self.expiry_date:
            days_left = (self.expiry_date - today).days

            if self.purchase_date:
                total_days = (self.expiry_date - self.purchase_date).days
                if total_days > 0:
                    percent = int(100 * (1 - (days_left / total_days)))
                    if percent < 10 and days_left > 0:
                        percent = 10
                else:
                    percent = 100
            else:
                percent = 100 if days_left < 0 else 10

            # Set color
            if days_left < 0:
                color = "danger"
            elif days_left < 90:
                color = "warning"
            else:
                color = "success"

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

# ---------- Assignments ----------

class LicenseAssignment(NetBoxModel):
    """Represents assignment of a license to a device OR a virtual machine."""

    license = models.ForeignKey(
        "License", on_delete=models.CASCADE, related_name="assignments"
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="license_assignments",
        null=True, blank=True
    )
    virtual_machine = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="license_assignments",
        null=True, blank=True
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.PROTECT, related_name="lm_assignments", null=True, blank=True
    )
    volume = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of license allocated. Only relevant for Volume Licenses."
    )
    assigned_to = models.DateTimeField(default=now)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    device_manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="device_license_assignments",
        null=True,
        blank=True
    )

    tags = TaggableManager(related_name="lm_assignment_tags")

    def clean(self):
        if self.device and self.virtual_machine:
            raise ValidationError("A license can only be assigned to either a Device or a Virtual Machine, not both.")
        if not self.device and not self.virtual_machine:
            raise ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if self.license:
            if not self.license.license_type:
                raise ValidationError("Selected license must be linked to a license type.")

            volume_type = self.license.license_type.volume_type

            self.manufacturer = self.license.manufacturer

            if volume_type == "single":
                if self.volume != 1:
                    raise ValidationError("Single licenses can only have a volume of 1.")
                existing_assignments = self.license.assignments.exclude(pk=self.pk).count()
                if existing_assignments >= 1:
                    raise ValidationError("Single licenses can only be assigned to one entity (Device or VM).")

            elif volume_type == "volume":
                if self.volume < 1:
                    raise ValidationError("Volume quantity must be at least 1.")
                total_assigned_volume = (
                    self.license.assignments.exclude(pk=self.pk)
                    .aggregate(models.Sum('volume'))['volume__sum'] or 0
                )
                if total_assigned_volume + self.volume > self.license.volume_limit:
                    raise ValidationError(
                        f"Exceeds volume limit ({self.license.volume_limit}). Currently assigned: {total_assigned_volume}."
                    )

        if self.device and not self.device_manufacturer:
            self.device_manufacturer = self.device.device_type.manufacturer

    clone_fields = [
        'manufacturer', 'license', 'device', 'virtual_machine', 'description',
    ]

    def __str__(self):
        return f"{self.license.license_key} → {self.device or self.virtual_machine} ({self.volume})"

    def get_absolute_url(self):
        return reverse("plugins:license_management:licenseassignment", args=[self.pk])
    
    class Meta:
        verbose_name = "License Assignments"
        verbose_name_plural = "License Assignments"
        