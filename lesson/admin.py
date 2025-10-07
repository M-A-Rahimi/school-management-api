from django.contrib import admin
from .models import Lesson, News, Exercise, ExerciseSubmission
# Register your models here.

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "lesson_teacher", "is_published", "created_at","updated_at")
    list_filter = ("is_published", "lesson_teacher__lesson__name", "created_at")
    search_fields = ("title", "text", "author__username", "lesson_teacher__lesson__name")
    autocomplete_fields = ("author", "lesson_teacher")
    ordering = ("-created_at",)



@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "lesson_teacher", "submission_deadline", "is_published", "created_at","updated_at")
    list_filter = ("is_published", "lesson_teacher__lesson__name", "created_at")
    search_fields = ("title", "text", "lesson_teacher__lesson__name", "author__username")
    autocomplete_fields = ("author", "lesson_teacher")
    ordering = ("-created_at",)



@admin.register(ExerciseSubmission)
class ExerciseSubmissionAdmin(admin.ModelAdmin):
    list_display = ("exercise", "student", "created_at", "updated_at")
    list_filter = ("exercise__lesson_teacher__lesson__name", "created_at")
    search_fields = ("exercise__title", "student__username", "student__first_name", "student__last_name")
    autocomplete_fields = ("exercise", "student")
    ordering = ("-created_at",)
