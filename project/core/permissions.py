from rest_framework import permissions

class MarketOwnerPermission(permissions.BasePermission):
    """
    Check the user market has market owner permission.
    """

    def has_permission(self, request, view):
        #TODO temporarily do it dynamicly
        #has_perm = MarketOwner.objects.filter(mobile=request.user.mobile).exists()
        has_perm = request.user.username == '+905535850117'
        return has_perm