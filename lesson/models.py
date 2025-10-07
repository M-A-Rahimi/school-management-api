from django.db import models
from school.models import LessonTeacher
from account.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.


def exercise_upload_path(instance, filename):
    return f"exercise/{instance.lesson_teacher.teacher.username}/{instance.lesson_teacher.lesson.name}/{filename}"

def exercise_submission_upload_path(instance, filename):
    return f"exercise/{instance.exercise.lesson_teacher.teacher.username}/{instance.exercise.lesson_teacher.lesson.name}/submissions/{filename}"


class Lesson(models.Model):
    name = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return F"lesson --- {self.name}"
    

class News(models.Model):
    author = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name = 'published_news')
    title = models.CharField(max_length = 100)
    text = models.TextField()
    lesson_teacher = models.ForeignKey(LessonTeacher,on_delete = models.CASCADE,related_name = "news")
    is_published = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"News --- {self.title} --- {self.lesson_teacher.lesson.name}"


class Exercise(models.Model):
    author = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name = 'published_exercise')
    title = models.CharField(max_length = 100)
    text = models.TextField()
    attachment = models.FileField(upload_to=exercise_upload_path,validators=[FileExtensionValidator(allowed_extensions=["zip", "pdf"])],blank=True,null=True,)
    submission_deadline = models.DateTimeField()
    lesson_teacher = models.ForeignKey(LessonTeacher,on_delete = models.CASCADE,related_name = "exercise")
    is_published = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"Exercise --- {self.title} --- {self.lesson_teacher.lesson.name}"
    

class ExerciseSubmission(models.Model):
    student = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'exercise_submissions')
    exercise = models.ForeignKey(Exercise,on_delete = models.CASCADE,related_name = 'submissions')
    text = models.TextField(blank=True,null=True)
    attachment = models.FileField(upload_to=exercise_submission_upload_path,validators=[FileExtensionValidator(allowed_extensions=["zip", "pdf"])],blank=True,null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return F"ExerciseSubmission --- {self.exercise.title} --- {self.student.get_full_name()}"
    
    class Meta:
        unique_together = ('student', 'exercise')