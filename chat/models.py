from django.db import models
from account.models import User
# Create your models here.

class Chat(models.Model):
    teacher = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'teacher_chats')
    student = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'student_chats')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return F"Chat --- {self.teacher.get_full_name()} --- {self.student.get_full_name()}"
    class Meta:
        unique_together = ('teacher', 'student')

class Message(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'messages')
    chat = models.ForeignKey(Chat,on_delete = models.CASCADE,related_name = 'messages')
    text = models.TextField()
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return F"Message --- {self.chat}"

    class Meta:
        ordering = ['created_at']