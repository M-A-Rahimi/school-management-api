from django.contrib import admin
from.models import School,LessonTeacher,ClassRoom,SchoolStudent,SchoolTeacher,LessonStudent
# Register your models here.

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name','management')
    search_fields = ('name','management__first_name','management__last_name')
    
@admin.register(LessonTeacher)
class LessonTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher__first_name','lesson__name')
    list_filter = ('lesson__name',)
    search_fields = ('teacher__first_name',)
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name','school__name')
    search_fields = ('name',)
    list_filter = ('school__name',)
    
    
@admin.register(SchoolStudent)
class SchoolStudentAdmin(admin.ModelAdmin):
    list_display = ('student','school','created_at','updated_at')
    
@admin.register(SchoolTeacher)
class SchoolTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher','school','created_at','updated_at')
    
@admin.register(LessonStudent)
class LessonStudentAdmin(admin.ModelAdmin):
    list_display = ('student','lesson_teacher','created_at','updated_at')
    