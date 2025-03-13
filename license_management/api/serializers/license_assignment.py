from rest_framework import serializers
from license_management.models import LicenseAssignment

class LicenseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseAssignment
        fields = "__all__"
