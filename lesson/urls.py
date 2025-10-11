from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LessonViewSet,
    LessonListView,
    NewsViewSet,
    ExerciseViewSet,
    ExerciseSubmissionStudentViewSet,
    ExerciseSubmissionTeacherListView
)

router = DefaultRouter()

# Lesson
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'lessons-list', LessonListView, basename='lesson-list')

# News
router.register(r'news', NewsViewSet, basename='news')

# Exercise
router.register(r'exercises', ExerciseViewSet, basename='exercise')

# Exercise Submission for Students
router.register(r'submissions', ExerciseSubmissionStudentViewSet, basename='exercise-submission')




urlpatterns = [
    path('', include(router.urls)),
    # Teacher view of submissions for a given exercise
    path('exercises/<int:pk>/submissions/', ExerciseSubmissionTeacherListView.as_view(), name='teacher-exercise-submissions'),
]
