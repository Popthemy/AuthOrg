from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from uuid import uuid4




class UserSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(max_length=36,source='id',read_only=True)
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone']


class RegisterUserSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=36, read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)
    phone = serializers.CharField(
        max_length=15, allow_blank=True, required=False)

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        errors = {}
        if not data.get('first_name'):
            errors['first_name'] = [
                {'field': 'first_name', 'message': 'First name is required'}]
        if not data.get('last_name'):
            errors['last_name'] = [
                {'field': 'last_name', 'message': 'Last name is required'}]
        if not email:
            errors['email'] = [
                {'field': 'email', 'message': 'Email is required'}]
        if not password:
            errors['password'] = [
                {'field': 'password', 'message': 'Password is required'}]

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                errors['password'] = [
                    {'field': 'password', 'message': f'str{e}'}]

        if User.objects.filter(email=email).exists():
            errors['email'] = [
                {'field': 'email', 'message': 'This email is already registered'}]

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            id=str(uuid4()), **validated_data
        )
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True, style={
                                     'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    return user
                raise serializers.ValidationError(
                    [{'field': 'password', 'message': 'Incorrect password'}])
            raise serializers.ValidationError(
                [{'field': 'email', 'message': 'Incorrect email'}])
        raise serializers.ValidationError(
            [{'field': 'email and password', 'message': 'Email and password cannot be empty'}])
