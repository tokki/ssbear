from django.urls import path, include

from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.index, name='index'),
    path('account/login/', views.login_view, name='login'),
    path('account/register/', views.register_view,name='register'),
    path('account/logout/', views.logout_view,name='logout'),
    path('account/send_code/', views.send_code_view,name='send-code'),
    path('account/reset_password/',views.reset_password_view,name='reset-password'),
    path('account/change_password/', views.change_password_view),
    path('account/change_email/', views.change_email_view),
    ]

