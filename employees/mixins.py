from django.core.exceptions import PermissionDenied
from .models import Employee

class OwnershipMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        current_user = self.request.user._wrapped if hasattr(self.request.user, '_wrapped') else self.request.user
        object_owner = getattr(self.get_object(), 'email')
        if str(current_user) != str(object_owner) and not current_user.is_staff:
            raise PermissionDenied
        return super(OwnershipMixin, self).dispatch(request, *args, **kwargs)