from rest_framework import permissions


class GlobalDefaultPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            model = view.get_queryset().model
        except Exception:
            return False

        action_map = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
            'OPTIONS': 'view',
            'HEAD': 'view',
        }

        action = action_map.get(request.method)

        if not action:
            return False

        perm = f'{model._meta.app_label}.{action}_{model._meta.model_name}'
        return request.user.has_perm(perm)
