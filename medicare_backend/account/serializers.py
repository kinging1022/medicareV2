from rest_framework import serializers
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
        print(validated_data)
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
        fields = ('id','email','first_name','last_name', 'dob' , 'gender','role')
