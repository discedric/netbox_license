from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ..choices import (
    VolumeTypeChoices,
    PurchaseModelChoices,
    LicenseModelChoices,
    VolumeRelationChoices,
)
class LicenseType(NetBoxModel):
    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)
    
    manufacturer = models.ForeignKey(
        to= 'dcim.Manufacturer',
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
        on_delete=models.PROTECT,
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
        return reverse("plugins:netbox_license:licensetype", args=[self.pk])
    
    class Meta:
        verbose_name = "License Type"
        verbose_name_plural = "License Types"