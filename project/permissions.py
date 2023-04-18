from rest_framework import permissions

#permission for readonly on dailyupte
class IsAdminStaffReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
            return True
        elif request.user.is_superuser or request.user.is_staff:
            return True
        else:
            return False
        
#permission Profile. owner can edit, others readonly (profile)
class ProfileOwnerReadOnly(permissions.BasePermission):                                   

    def has_object_permission(self, request, view, obj):
        if(request.method in permissions.SAFE_METHODS):
            return True
        
        return request.user == obj.user


#Permission on Daily update. owner can edit, others readonly (dailyUpdate)
class DailyUpdateOwnerCanEdit(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['PUT', 'PATCH']:
            return obj.account == request.user
        else:
            return False

#permission Profile
class ProfileOwnerCanEdit(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['PUT', 'PATCH']:
            return obj.user == request.user
        else:
            return False