from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LoginView.as_view(), name='logout'),
    path('validate_username', csrf_exempt(views.UsernameValidationView.as_view()), name='validate_username'),
    path('validate_email', csrf_exempt(views.EmailValidationView.as_view()), name='validate_email'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('password_reset', views.RequestPasswordResetEmail.as_view(), name='password_reset'),
    path('set_new_password/<uidb64>/<token>', views.CompletePasswordReset.as_view(), name='reset_user_password'),
]