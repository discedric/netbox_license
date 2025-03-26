from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from license_management.models import License, LicenseAssignment

class LicenseSerializer(NetBoxModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


class LicenseAssignmentSerializer(NetBoxModelSerializer):
    license = LicenseSerializer(nested=True, required=True)
    class Meta:
        model = LicenseAssignment
        fields = '__all__'
