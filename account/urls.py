from django.urls import path, include

from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('send-code/', views.SendCode.as_view(), name='send-code'),
    path('reset-password/', views.ResetPassword.as_view(), name='reset-password'),
    path('change-password/', views.ChangePassword.as_view()),
    path('change-email/', views.ChangeEmail.as_view()),
]
