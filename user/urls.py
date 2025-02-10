from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apis.views import (ActivateView, LogoutView, PasswordResetConfirmView,
                         PasswordResetRequestView, RegistrationView,SignInView,View_Support)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate-email'),
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('login/', SignInView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('support/', View_Support.as_view(), name='View_Support'),
    
]
