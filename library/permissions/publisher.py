from rest_framework.permissions import BasePermission


class CanViewStatistic(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('can_view_statistic')
