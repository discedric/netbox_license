from rest_framework import serializers
from license_management.models import License

class LicenseSerializer(serializers.ModelSerializer):
    """Serializer for the License model"""

    display = serializers.SerializerMethodField()

    class Meta:
        model = License
        fields = ["id", "name", "license_key", "manufacturer", "description", "display"]

    def get_display(self, obj):
        """Format display field to include name and description"""
        if obj.description:
            return f"{obj.name}"
        return obj.name 
