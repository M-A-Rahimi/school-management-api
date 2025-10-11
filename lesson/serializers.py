from rest_framework import serializers
from.models import News,Exercise,ExerciseSubmission
from account.serializers import UserSerializer
from school.serializers import ListLessonTeacherSerializer
from django.utils import timezone
 


class NewsCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = News
        fields = '__all__'
        
class NewsListSerializer(serializers.ModelSerializer):
    lesson_teacher =  ListLessonTeacherSerializer()
    class Meta:
        model = News
        fields = ['id','title','text','lesson_teacher','created_at']
        
class NewsDetailSerializer(NewsCreateSerializer):
    lesson_teacher = ListLessonTeacherSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    
    
    
    
    
class ExerciseCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = Exercise
        fields = '__all__'
        
class ExerciseListSerializer(serializers.ModelSerializer):
    lesson_teacher =  ListLessonTeacherSerializer()
    class Meta:
        model = Exercise
        fields = ['id','title','text','lesson_teacher','attachment','submission_deadline','created_at']
        
class ExerciseDetailSerializer(NewsCreateSerializer):
    lesson_teacher = ListLessonTeacherSerializer(read_only=True)
    author = UserSerializer(read_only=True)



class ExerciseSubmissionCreateSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ExerciseSubmission
        fields = '__all__'

class ExerciseSubmissionListSerializer(serializers.ModelSerializer):
    exercise = ExerciseListSerializer(read_only=True)  # nested exercise

    class Meta:
        model = ExerciseSubmission
        fields = ['id','exercise','text','attachment','created_at','updated_at']

class ExerciseSubmissionDetailSerializer(ExerciseSubmissionCreateSerializer):
    exercise = ExerciseListSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    
class TeacherExerciseSubmissionDetailSerializer(serializers.ModelSerializer):
    submissions = ExerciseSubmissionDetailSerializer(many = True)

    class Meta:
        model = Exercise
        fields = ['title','text','attachment','submissions']
    