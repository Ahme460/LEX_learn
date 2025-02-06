from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import EmailMessage
from django.conf import settings
from ..models import Account,UserDevice


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    device_id=serializers.CharField(write_only=True,required=True)

    class Meta:
        model = Account
        fields = [ 'email', 'username', 'phone_number', 'country', 'birth_date', 'password',"device_id"]
        
        
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        password = validated_data.pop('password', None)
        user = Account.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        if not UserDevice.objects.filter(device_id=device_id).exists():
            seasion_user=UserDevice.objects.create(
                user=user,
            device_id=device_id
            )
            seasion_user.save()
        else:
            raise ValueError({"eroor":"this device is exist"})
        return user

    

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    device_id=serializers.CharField(write_only=True,required=True)
    

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        device_id=data.get('device_id',None)

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")

        if not device_id:
            raise ValueError("device_id is required")
        
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials or user does not exist")

        if not user.is_active:
            raise AuthenticationFailed("User account is deactivated")

        if not UserDevice.objects.filter(user=user, device_id=device_id).exists():
            user.is_active = False  # تعطيل الحساب
            user.save()
            sent_email = EmailMessage(
                subject='Disable your account',
                body=f'Disable account You are trying to access your account from an unauthorized device',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            raise ValidationError({"code": "unauthorized_device", "error": "You are trying to access your account from an unauthorized device"})

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

