from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import Group

class UserGroupsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user_groups = request.user.groups.all()
        else:
            request.user_groups = []
