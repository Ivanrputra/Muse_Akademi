from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS,IsAuthenticatedOrReadOnly

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        # return request.method in SAFE_METHODS
        if request.method in SAFE_METHODS:
            return True
        return False