from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Employee

class OwnershipMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        current_user = self.request.user._wrapped if hasattr(self.request.user, '_wrapped') else self.request.user
        employee = Employee.objects.get(pk=self.kwargs.get('pk'))
        object_owner = getattr(employee, 'email')
        if str(current_user) != str(object_owner) and not current_user.is_staff:
            raise PermissionDenied
        return super(OwnershipMixin, self).dispatch(request, *args, **kwargs)

class StaffUserMixin(PermissionRequiredMixin):
    permission_required = 'MyUser.is_staff'