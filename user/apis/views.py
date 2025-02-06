from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import Account
from .serializers import (PasswordResetConfirmSerializer,
                          RegistrationSerializer, CustomTokenObtainPairSerializer)


class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active=False
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f'https://alex-medlearn.netlify.app/activate/{uid}/{token}'
            email = user.email

            sent_email = EmailMessage(
                subject='Activation Email',
                body=f'Please click the link to activate your account: {activation_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )

            sent_email.send()
            return Response({
                "message": "Account created successfully, check your email to activate it.",
                "user":serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
      
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({
                        "message": "Account activated successfully."}, status=status.HTTP_200_OK)
        
            return Response({'error': 'Invalid or expired activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Account.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def getResponseToken(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return Response({
        'access': access_token,
        'refresh': refresh_token
    }, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"https://alex-medlearn.netlify.app/password-reset-confirm/{uid}/{token}/"

        try:
            email_message = EmailMessage(
                subject="Password Reset Request",
                body=f"Click the link below to reset your password:\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_message.send(fail_silently=False)

        except Exception as e:
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Password reset link sent successfully"}, status=status.HTTP_200_OK)
    

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data, context={'uidb64': uidb64, 'token': token})
        if serializer.is_valid():
            serializer.save()

            return Response(
                {'message': 'Password reset successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid data'},
                status=status.HTTP_400_BAD_REQUEST
            )
