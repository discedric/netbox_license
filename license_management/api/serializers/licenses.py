from rest_framework import serializers
from license_management.models import License

class LicenseSerializer(serializers.ModelSerializer):
    """Serializer for the License model"""

    class Meta:
        model = License
        fields = '__all__'
