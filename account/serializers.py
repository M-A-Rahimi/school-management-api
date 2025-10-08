from rest_framework import serializers
from .models import QueueSignUp
from account.models import User



class QueueSignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QueueSignUp
        exclude = ['created_at', 'updated_at']
        read_only_fields = [] 

    def __init__(self, *args, **kwargs):
        """
            Customize serializer fields based on the requesting user.

            Functionality:
                - Called automatically when the serializer instance is created.
                - Accesses the current user from self.context['request'].user.
                - If the user is a superuser:
                    - All fields are writable (read_only_fields = []).
                - If the user is not a superuser:
                    - 'status' and 'rejection_reason' fields are set as read-only.
                    - Prevents normal users from approving/rejecting requests.
        """
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        
        if user.is_superuser:
            self.Meta.read_only_fields = []
        else:
            self.Meta.read_only_fields = ['status', 'rejection_reason']
            

    def validate_national_code(self, value):

        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("National code must be 10 digits.")

        if User.objects.filter(national_code=value).exists():
            raise serializers.ValidationError("This national code already exists in the system!")

        check = int(value[9])
        s = sum(int(value[i]) * (10 - i) for i in range(9))
        remainder = s % 11
        if (remainder < 2 and check != remainder) or (remainder >= 2 and check != 11 - remainder):
            raise serializers.ValidationError("Invalid national code.")

        return value
    
    
    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("This email already exists in the system!")
        return value