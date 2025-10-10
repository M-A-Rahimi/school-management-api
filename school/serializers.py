from rest_framework import serializers
from .models import School,ClassRoom,LessonTeacher,SchoolTeacher,SchoolStudent,SchoolTeacher
from account.models import User
from account.serializers import UserSerializer
from lesson.serializers import LessonSerializer

class SchoolListCreateSerializer(serializers.ModelSerializer):    
    management = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(status='m'),write_only=True)

    management_detail = UserSerializer(source='management', read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'management', 'management_detail', 'created_at', 'updated_at']
    
    # def validate_management(self,value):
    #     print(value)
    #     if not User.objects.filter(id = value,status = 'm').exists():
    #         raise serializers.ValidationError("Only users with role 'm' (manager) can be assigned as management.")
        
    #     return value
    
    
class SchoolStudentSerializer(serializers.ModelSerializer):
    student =  UserSerializer()
    class Meta:
        model = SchoolStudent
        fields = ['student']

class SchoolTeacherSerializer(serializers.ModelSerializer):
    teacher =  UserSerializer()
    class Meta:
        model = SchoolTeacher
        fields = ['teacher']

    
class SchoolRetrieveSerializer(serializers.ModelSerializer):    
    teachers =  SchoolTeacherSerializer(many = True)
    students =  SchoolStudentSerializer(many = True)
    class Meta:
        model = School
        fields = ['id','name','teachers','students','created_at','updated_at']

class CreateUpdateClassRoomSerializer(serializers.ModelSerializer):    

    class Meta:
        model = ClassRoom
        fields = ['id','name','school','lesson_teachers']
    

    def validate(self, attrs):
        school = getattr(self.instance, 'school', None)
        """
            Ensure that the lesson teachers being added belong to the same school as the class.
            This restriction applies to all users, including superusers.
        """
        lesson_teachers = attrs.get('lesson_teachers', [])
        for lt in lesson_teachers:
            
            if not SchoolTeacher.objects.filter(teacher=lt.teacher, school=school).exists() or not lt.teacher.status == 't':
                raise serializers.ValidationError(
                    f"Teacher {lt.teacher.username} does not belong to the school of this class."
                )
        return attrs
        
class ListLessonTeacherSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    teacher = UserSerializer() 
    class Meta:
        model = LessonTeacher
        fields = ['id','lesson','teacher','created_at','updated_at']
    
class LessonTeacherClassRoom(serializers.ModelSerializer):
    lesson = LessonSerializer()
    teacher = UserSerializer() 
    students = UserSerializer(many = True)
    class Meta:
        model = LessonTeacher
        fields = ['id','lesson','teacher','students','created_at','updated_at']
        
class ListClassRoomSerializer(serializers.ModelSerializer):
    lesson_teachers = LessonTeacherClassRoom(many = True)
    class Meta:
        model = ClassRoom
        fields = ['id','name','lesson_teachers']
        
class SchoolClassRoomSerializer(serializers.ModelSerializer):
    class_rooms = ListClassRoomSerializer(many = True)
    class Meta:
        model = School
        fields = ['id','class_rooms']