from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        #check if the requesting user is the owner
        if request.method in permissions.SAFE_METHODS:
            #For, GET, HEAD, and OPTIONS requests, anyone can access
            return True
        else:
            #For POST, PUT, PATCH and DELETE request, only the owner can access
            return obj.user == request.user


class UpdateIsOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        #check if the requesting user is the owner
        if request.method in permissions.SAFE_METHODS:
            #For, GET, HEAD, and OPTIONS requests, anyone can access
            return True
        else:
            #For POST, PUT, PATCH and DELETE request, only the owner can access
            return obj.owner == request.user
        

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        #if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and request.user.role=='admin':
       #     return True
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.role=='admin'

class IsReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        else:
            return obj.announcementID == request.user