from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        user = User(**data)
        password = data.get('password')
        
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


# class UserCreateSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
    
#     def validate(self, data):
#         user = User(**data)
#         password = data.get('password')
        
#         try:
#             validate_password(password, user)
#         except exceptions.ValidationError as e:
#             serializer_errors = serializers.as_serializer_error(e)
#             raise serializers.ValidationError(
#                 {'password': serializer_errors['non_field_errors']}
#             )
        
#         return data
    
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user
