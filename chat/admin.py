from django.contrib import admin
from.models import Chat,Message
# Register your models here.



@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher__first_name', 'student__first_name', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat')
    