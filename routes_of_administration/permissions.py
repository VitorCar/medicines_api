from rest_framework import permissions


class RoutesAdministrationPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('routes_of_administration.view_routesofadministration')

        if request.method == 'POST':
            return request.user.has_perm('routes_of_administration.add_routesofadministration')
        return False
