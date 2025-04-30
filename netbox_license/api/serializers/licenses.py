from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_license.models import License, LicenseAssignment, LicenseType


class LicenseTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = LicenseType
        fields = '__all__'


class LicenseSerializer(NetBoxModelSerializer):
    license_type = LicenseTypeSerializer(nested=True, required=True)
    class Meta:
        model = License
        fields = '__all__'


class LicenseAssignmentSerializer(NetBoxModelSerializer):
    license = LicenseSerializer(nested=True, required=True)
    class Meta:
        model = LicenseAssignment
        fields = '__all__'

