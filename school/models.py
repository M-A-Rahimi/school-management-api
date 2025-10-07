from django.db import models
from account.models import User
# Create your models here.


class School(models.Model):
    name = models.CharField(max_length = 50)
    management = models.OneToOneField(User,on_delete = models.PROTECT,related_name = 'school')
    teachers = models.ManyToManyField(User,blank = True,related_name = 'schools')
    students = models.ManyToManyField(User,blank = True,related_name = '+')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return F"School --- {self.name} --- {self.management.first_name} {self.management.last_name}"



class LessonTeacher(models.Model):
    teacher = models.ForeignKey(User,on_delete = models.PROTECT,related_name = 'lesson')
    lesson = models.ForeignKey('lesson.Lesson',on_delete = models.CASCADE,related_name = 'teachers')
    students = models.ManyToManyField(User, blank=True, related_name='lesson_teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"LessonTeacher --- {self.lesson.name} --- {self.teacher.first_name} {self.teacher.last_name}"
    
    class Meta:
        unique_together = ("lesson", "teacher")
    
class ClassRoom(models.Model):
    name = models.CharField(max_length = 50)
    school = models.ForeignKey(School,on_delete = models.CASCADE,related_name = 'class_rooms')
    lesson_teachers = models.ManyToManyField(LessonTeacher,blank = True,related_name = 'class_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return F"ClassRoom --- {self.name} --- {self.school.name}"
