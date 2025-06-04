from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_license.models.license import License
from netbox_license.models.licenseassignment import LicenseAssignment
from netbox_license.models.licensetype import LicenseType
from dcim.api.serializers import (
    DeviceSerializer,
    DeviceTypeSerializer,
    ManufacturerSerializer,
)
from virtualization.api.serializers import (
    VirtualMachineSerializer,
    ClusterSerializer,
)
from rest_framework.serializers import SerializerMethodField

class LicenseTypeSerializer(NetBoxModelSerializer):
    manufacturer = ManufacturerSerializer(nested=True, required=True)
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
    device = DeviceSerializer(nested=True, required=False)
    device_type = DeviceTypeSerializer(nested=True, required=False)
    virtual_machine = VirtualMachineSerializer(nested=True, required=False)

    class Meta:
        model = LicenseAssignment
        fields = '__all__'

    
