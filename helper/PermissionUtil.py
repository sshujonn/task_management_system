from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import exceptions


def check_permission(request, action, module):
    try:
        name = module[1]
        groups = User.objects.get(pk=request.user.id).groups.all()
        if action == ("detail" or "view") or module[0] == "view":
            codename = "view_{name}".format(name=name)
        elif action == "update":
            codename = "change_{name}".format(name=name)
        elif action == "delete":
            codename = "delete_{name}".format(name=name)
        elif module[0] == "create":
            codename = "add_{name}".format(name=name)
        else:
            # import pdb;
            # pdb.set_trace()
            return False
        permission = False
        for group in groups:
            permission = permission or group.permissions.filter(codename=codename).exists()
        # import pdb;pdb.set_trace()
        return permission
    except Exception as ex:
        # import pdb;
        # pdb.set_trace()
        return False


class DBCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        action = request.resolver_match.kwargs.get('action')
        module = request.resolver_match.url_name.split("_")

        return check_permission(request, action, module)
