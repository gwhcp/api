from rest_framework import permissions


class DjangoPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class GaclPermissions(permissions.BasePermission):
    """
    Fine tune permissions.
    """

    def has_permission(self, request, view):
        perms = getattr(view, "gacl", {})

        if request.method == 'GET' and 'view' in perms:
            for perm in perms['view']:
                return request.user.has_perm(perm)

        elif request.method == 'POST' and 'add' in perms:
            for perm in perms['add']:
                return request.user.has_perm(perm)

        elif (request.method == 'PATCH' or request.method == 'PUT') and 'change' in perms:
            for perm in perms['change']:
                return request.user.has_perm(perm)

        elif request.method == 'DELETE' and 'delete' in perms:
            for perm in perms['delete']:
                return request.user.has_perm(perm)

        return True
