from rest_framework.permissions import IsAuthenticated

class IsSuperUser(IsAuthenticated):
    def has_permission(self, request, view):
        return  request.user.is_superuser
    
class IsManagement(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.status == 'm'


class IsTeacher(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.status == 't'


class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.status == 's'