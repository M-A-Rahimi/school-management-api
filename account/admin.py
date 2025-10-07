from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,QueueSignUp

# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        ('My Fields', {'fields': ('status','national_code','bio')}),
    )

    list_display = UserAdmin.list_display + ('status',)
    search_fields = UserAdmin.search_fields + ('national_code',)
    list_filter = UserAdmin.list_filter + ('status',)

@admin.register(QueueSignUp)
class QueueSignUpAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','role','status')
    search_fields = ('national_code','first_name','last_name')
    list_filter = ('status','role')