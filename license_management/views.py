from django.shortcuts import render
from .models import SoftwareLicense

def list_licenses(request):
    licenses = SoftwareLicense.objects.all()
    return render(request, 'software_license_management/list_licenses.html', {'licenses': licenses})
