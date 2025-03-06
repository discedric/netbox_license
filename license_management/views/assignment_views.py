from netbox.views import generic
from ..models import LicenseAssignment
from ..forms import LicenseAssignmentForm
from ..tables import LicenseAssignmentTable
from ..filtersets import LicenseAssignmentFilterSet

class LicenseAssignmentListView(generic.ObjectListView):
    """View to list all license assignments."""
    queryset = LicenseAssignment.objects.all()
    table = LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet

class LicenseAssignmentDetailView(generic.ObjectView):
    """View to show details of a specific license assignment."""
    queryset = LicenseAssignment.objects.all()

class LicenseAssignmentEditView(generic.ObjectEditView):
    """View to add or edit a license assignment."""
    queryset = LicenseAssignment.objects.all()
    form = LicenseAssignmentForm

class LicenseAssignmentDeleteView(generic.ObjectDeleteView):
    """View to delete a license assignment."""
    queryset = LicenseAssignment.objects.all()
