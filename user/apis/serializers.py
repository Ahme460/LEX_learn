from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from ..models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [ 'email', 'username', 'phone_number', 'country', 'birth_date', 'password']
        

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Account.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
        
        user.save()

        return user
    

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials or user does not exist")

        if not user.is_active:
            raise AuthenticationFailed("User account is deactivated")
        data['user'] = user
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True,min_length=8)
    confirm_new_password = serializers.CharField(write_only=True, required=True,min_length=8)

    def validate(self, data):
        uidb64 = self.context['uidb64']
        token = self.context['token']

        if data['new_password'] != data['confirm_new_password']:
            raise ValidationError(
                {'confirm_new_password': 'The new passwords do not match'}
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (Account.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError(
                {'token': 'Invalid token '}
            )
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({'token': 'Invalid or expired token'})

        return data

    def save(self):
        uidb64 = self.context['uidb64']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

