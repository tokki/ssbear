from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('download/', views.download),
    path('announcement/', views.announcement_detail),
    path('buy/', views.buy),
    path('confirm/', views.confirm),
    path('pay/', views.pay),
    path('pay/code/', views.codepay),
    path('my_service/', views.my_service),
    path('info/', views.info),
    path('invite_history/', views.invite_history),
    path('add_invite/', views.add_invite),
    path('bill/', views.bill),
    path('order/<int:id>/', views.order),
    path('chart/', views.chart),
    path('change_ss_password/<int:oid>/', views.change_ss_password),
    path('change_uuid/<int:oid>/', views.change_uuid),
]
