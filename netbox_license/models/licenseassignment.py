from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Device
from virtualization.models import VirtualMachine
from django.utils.timezone import now
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from ..choices import AssignmentKindChoices

class LicenseAssignment(NetBoxModel):

    license = models.ForeignKey(
        "License", on_delete=models.CASCADE, related_name="assignments",
        null=True, blank=True
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="license_assignments",
        null=True, blank=True
    )
    virtual_machine = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="license_assignments",
        null=True, blank=True
    )
    
    volume = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of license allocated. Only relevant for Volume Licenses."
    )
    assigned_on = models.DateTimeField(default=now)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


    tags = TaggableManager(related_name="lm_assignment_tags")

    @property
    def kind(self):
        if self.device_id:
            return AssignmentKindChoices.DEVICE
        elif self.virtual_machine_id:
            return AssignmentKindChoices.VM
        return None

    def get_kind_display(self):
        return dict(AssignmentKindChoices).get(self.kind)

    @property
    def assigned_object(self):
        return self.device or self.virtual_machine

    def clean(self):
        if self.device and self.virtual_machine:
            raise ValidationError("A license can only be assigned to either a Device or a Virtual Machine, not both.")
        if not self.device and not self.virtual_machine:
            raise ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if self.license:
            if not self.license.license_type:
                raise ValidationError("Selected license must be linked to a license type.")

            volume_type = self.license.license_type.volume_type

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

        
    clone_fields = [
        'license', 'device', 'virtual_machine', 'description',
    ]

    def __str__(self):
        license_key = getattr(self.license, "license_key", "Missing license")
        assigned_obj = self.assigned_object or "Unassigned"
        return f"{license_key} → {assigned_obj} ({self.volume})"



    def get_absolute_url(self):
        return reverse("plugins:netbox_license:licenseassignment", args=[self.pk])

    class Meta:
        verbose_name = "License Assignments"
        verbose_name_plural = "License Assignments"
        constraints = [
            models.CheckConstraint(
                check=models.Q(device__isnull=False) | models.Q(virtual_machine__isnull=False),
                name='licenseassign_either_device_or_vm_required'
            ),
            models.CheckConstraint(
                check=~(models.Q(device__isnull=False) & models.Q(virtual_machine__isnull=False)),
                name='licenseassign_only_one_target_allowed'
            )
        ]