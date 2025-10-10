from rest_framework import generics,filters
from django.db.models import Subquery
from account.permission import IsSuperUser,IsManagement
from .serializers import SchoolListCreateSerializer,CreateUpdateClassRoomSerializer,ListLessonTeacherSerializer,SchoolRetrieveSerializer,SchoolClassRoomSerializer
from .models import School,ClassRoom ,LessonTeacher,SchoolTeacher
# Create your views here.


class SchoolListCreateView(generics.ListCreateAPIView):
    """
        Handles listing all schools and creating a new school.
        Access is restricted to superusers only.
    """
    permission_classes = [IsSuperUser]
    serializer_class = SchoolListCreateSerializer
    queryset = School.objects.all()
    
class SchoolUpdateView(generics.UpdateAPIView):
    """
        Allows superusers to update the details of an existing school.
        Access is restricted to superusers only.
    """
    permission_classes = [IsSuperUser]
    serializer_class = SchoolListCreateSerializer
    queryset = School.objects.all()


class SchoolDetailListView(generics.ListAPIView):
    """
        Returns a list of a specific school along with its teachers and students.
        Access is restricted to school managers or superusers.
        Supports searching by teacher or student username.
    """
    permission_classes = [IsManagement]
    serializer_class = SchoolRetrieveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['teachers__teacher__username','students__student__username',]
    
    def get_queryset(self):
        return School.objects.filter(id = self.kwargs['id']).prefetch_related('teachers__teacher','students__student') if self.request.user.is_superuser \
        else School.objects.filter(id = self.kwargs['id'],management = self.request.user).prefetch_related('teachers__teacher','students__student')

class ClassRoomCreateView(generics.CreateAPIView):
    """
        Allows school management users to create new classrooms.
        Access is restricted to school managers and superusers.
    """
    permission_classes = [IsManagement]
    serializer_class = CreateUpdateClassRoomSerializer
    queryset = ClassRoom.objects.all()
    
class ListLessonTeacherView(generics.ListAPIView):
    """
        Returns a list of available teachers along with their lessons for adding to a classroom.
        Access is restricted to school managers and superusers.
        Supports searching by teacher username, lesson name, and school name.
    """
    permission_classes = [IsManagement]
    serializer_class = ListLessonTeacherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['teacher__username','lesson__name','school__name']
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return LessonTeacher.objects.select_related('teacher','lesson').all()
        
        teachers_in_user_schools = SchoolTeacher.objects.filter(school__management=self.request.user).values('teacher_id')
        
        return LessonTeacher.objects.select_related('teacher','lesson').filter(teacher__in=Subquery(teachers_in_user_schools))

class ClassRoomUpdateView(generics.UpdateAPIView):
    """
        Allows school management users to update classroom details, including adding teachers with lessons.
        Access is restricted to school managers and superusers.
    """

    permission_classes = [IsManagement]
    serializer_class = CreateUpdateClassRoomSerializer
    
    def get_queryset(self):
        return ClassRoom.objects.all() if self.request.user.is_superuser else ClassRoom.objects.filter(school__management = self.request.user) 


class SchoolClassRoomView(generics.ListAPIView):
    """
        Retrieves a list of classrooms for a specific school, including associated lessons, teachers, and students.
        Access is restricted to school managers and superusers.
    """
    permission_classes = [IsManagement]
    serializer_class = SchoolClassRoomSerializer
    
    def get_queryset(self):
        
        school_qs = School.objects.filter(id=self.kwargs['id'])
        
        if not self.request.user.is_superuser:
            school_qs = school_qs.filter(management=self.request.user)

        school_qs = school_qs.prefetch_related(
            'class_rooms',
            'class_rooms__lesson_teachers',
            'class_rooms__lesson_teachers__lesson',
            'class_rooms__lesson_teachers__teacher',
            'class_rooms__lesson_teachers__students',
        )
        return school_qs
