from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from .models import Employee

class OwnershipMixin(object):

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
        employee = Employee.objects.get(pk=kwargs.get('pk'))
        object_owner = getattr(employee, 'email')
        if str(current_user) != str(object_owner) and not current_user.is_staff:
            return HttpResponseRedirect('../')
        return super(OwnershipMixin, self).dispatch(request, *args, **kwargs)

class StaffRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect('../')
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class MonthOwnershipMixin(object):

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
        employee = self.get_object().employee
        object_owner = getattr(employee, 'email')
        if str(current_user) != str(object_owner):
            return HttpResponseRedirect('../')
        return super(MonthOwnershipMixin, self).dispatch(request, *args, **kwargs)
