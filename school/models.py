from django.db import models
from account.models import User
# from django.contrib.gis.db import models as gis_models
# Create your models here.


class School(models.Model):
    name = models.CharField(max_length = 50)
    management = models.OneToOneField(User,on_delete = models.PROTECT,related_name = 'management_school')
    # location = gis_models.PointField(srid=4326, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return F"School --- {self.name} --- {self.management.first_name} {self.management.last_name}"


class SchoolStudent(models.Model):
    student = models.OneToOneField(User,on_delete = models.CASCADE,related_name = 'student_school')
    school = models.ForeignKey(School,on_delete = models.PROTECT,related_name = 'students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Student {self.student.username} - School {self.school.name}"
    
    class Meta:
        unique_together = ("school",)
        

class SchoolTeacher(models.Model):
    teacher = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'teacher_schools')
    school = models.ForeignKey(School,on_delete = models.PROTECT,related_name = 'teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Teacher {self.teacher.username} - School {self.school.name}"

    class Meta:
        unique_together = ("teacher", "school")        


class LessonTeacher(models.Model):
    teacher = models.ForeignKey(User,on_delete = models.PROTECT,related_name = 'teacher_lessons')
    lesson = models.ForeignKey('lesson.Lesson',on_delete = models.CASCADE,related_name = 'teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"LessonTeacher --- {self.lesson.name} --- {self.teacher.first_name} {self.teacher.last_name}"
    
    class Meta:
        unique_together = ("lesson", "teacher")
        
class LessonStudent(models.Model):
    student = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'student_lessons')
    lesson_teacher = models.ForeignKey(LessonTeacher,on_delete = models.CASCADE,related_name = 'students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Student {self.student.username} - Lesson {self.lesson_teacher.lesson.name}"
    
    class Meta:
        unique_together = ("student", "lesson_teacher")
    
class ClassRoom(models.Model):
    name = models.CharField(max_length = 50)
    school = models.ForeignKey(School,on_delete = models.CASCADE,related_name = 'class_rooms')
    lesson_teachers = models.ManyToManyField(LessonTeacher,blank = True,related_name = 'class_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return F"ClassRoom --- {self.name} --- {self.school.name}"

    # class Meta:
    #     unique_together = ("name", "school")