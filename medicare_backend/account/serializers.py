from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    
    retype_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','email','first_name','last_name', 'dob' , 'gender','password','retype_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

   

    def create(self, validated_data):
        validated_data.pop('retype_password')
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            dob = validated_data['dob'],
            gender = validated_data['gender'],
            password = validated_data['password']

        )

        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = (
            'display_age',
            'unread_notification_count',
        )
        fields = ('id','email','first_name','dob','last_name', 'display_age' , 'gender','role','height',
                  'weight','allergies','blood_type','emergency_contact','unread_notification_count')



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise Exception('No active account found with the given credentials')
            
            if not user.is_active:
                raise Exception('Account is inactive')
            
        except User.DoesNotExist:
            raise Exception('No active account found with the given credentials')


        data = super().validate(attrs)
        return data