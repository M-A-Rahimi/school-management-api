from rest_framework import viewsets,mixins,generics,filters
from rest_framework import serializers
from django.utils import timezone
from account.permission import IsManagement,IsTeacher,IsStudent
from .school_serializers import LessonSerializer
from .serializers import NewsCreateSerializer,NewsListSerializer,NewsDetailSerializer,\
    ExerciseCreateSerializer,ExerciseDetailSerializer,ExerciseListSerializer,ExerciseSubmissionCreateSerializer,\
ExerciseSubmissionListSerializer,ExerciseSubmissionDetailSerializer,TeacherExerciseSubmissionDetailSerializer
from .models import Lesson,News,Exercise,ExerciseSubmission


class LessonViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsManagement]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    
class LessonListView(mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsTeacher,IsManagement]
    serializer_class = LessonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    queryset = Lesson.objects.all()
    
class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacher,IsManagement,IsStudent]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    serializer_classes = {'create': NewsCreateSerializer,'retrieve': NewsDetailSerializer,'list': NewsListSerializer}
    default_serializer_class = NewsCreateSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        user = self.request.user
        
        news_qs = News.objects.all()

        if not self.action == 'list':
            news_qs = News.objects.filter(id = self.kwargs['pk'])
        
        
        if user.status == 'm':
            news_qs = news_qs.filter(lesson_teacher__teacher__teacher_schools__school__management_in = user)
        
        if user.status == 't':
           news_qs =  news_qs.filter(lesson_teacher__teacher = user)
           
        if user.status == 's':
            return News.objects.filter(lesson_teacher__students_in = user)
        
        return news_qs
    


class ExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacher,IsManagement,IsStudent]

    serializer_classes = {'create': ExerciseCreateSerializer,'retrieve': ExerciseDetailSerializer,'list': ExerciseListSerializer}
    default_serializer_class = ExerciseCreateSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        user = self.request.user
        
        exercise_qs = Exercise.objects.all()

        if not self.action == 'list':
            exercise_qs = Exercise.objects.filter(id = self.kwargs['pk'])
                
        if user.status == 't':
           exercise_qs =  exercise_qs.filter(lesson_teacher__teacher = user)
           
        if user.status == 's':
            return Exercise.objects.filter(lesson_teacher__students_in = user)
        
        return exercise_qs

class ExerciseSubmissionStudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStudent]

    serializer_classes = {'create': ExerciseSubmissionCreateSerializer,'retrieve': ExerciseSubmissionDetailSerializer ,'list': ExerciseSubmissionListSerializer}
    default_serializer_class = ExerciseSubmissionCreateSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        user = self.request.user
                   
        if user.status == 's':
            return user.exercise_submissions.all()
        
        return ExerciseSubmission.objects.all()

    def perform_create(self, serializer):
        exercise = serializer.validated_data.get('exercise')
        if exercise.submission_deadline < timezone.now():
            raise serializers.ValidationError("The submission deadline has passed. You cannot submit.")
        serializer.save(student=self.request.user)

    def perform_update(self, serializer):
        exercise = serializer.instance.exercise
        if exercise.submission_deadline < timezone.now():
            raise serializers.ValidationError("The submission deadline has passed. You cannot edit this submission.")
        serializer.save()
        
    def perform_destroy(self, instance):
        exercise = instance.exercise
        if exercise.submission_deadline < timezone.now():
            raise serializers.ValidationError("The submission deadline has passed. You cannot edit this submission.")
        instance.delete()


class ExerciseSubmissionTeacherListView(generics.ListAPIView):
    permission_classes = [IsTeacher]
    serializer_class = TeacherExerciseSubmissionDetailSerializer
    def get_queryset(self):
        return Exercise.objects.filter(id = self.kwargs['pk'], lesson_teacher__teacher=self.request.user).prefetch_related('submissions')