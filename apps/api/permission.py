from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS,IsAuthenticatedOrReadOnly

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        # return request.method in SAFE_METHODS
        if request.method in SAFE_METHODS:
            return True
        return False

class IsMentorOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.mentor == request.user

class IsAdminOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.admin == request.user

class IsMentorOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_mentor or request.user.is_staff : 
            return True
        return False