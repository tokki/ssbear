from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('download/', views.Download.as_view()),
    path('announcement/', views.AnnouncementDetail.as_view()),
    path('buy/', views.Buy.as_view()),
    path('confirm/', views.Confirm.as_view()),
    path('pay/', views.Pay.as_view()),
    path('pay/code/', views.Codepay.as_view()),
    path('pay/alipay_page/', views.AlipayPage.as_view()),
    path('my_service/', views.MyService.as_view()),
    path('info/', views.Info.as_view()),
    path('invite_history/', views.InviteHistory.as_view()),
    path('add_invite/', views.AddInvite.as_view()),
    path('bill/', views.BillInfo.as_view()),
    path('order/<int:oid>/', views.OrderInfo.as_view()),
    path('chart/', views.Chart.as_view()),
    path('change_ss_password/<int:oid>/', views.SSPassword.as_view()),
    path('change_uuid/<int:oid>/', views.V2rayPassword.as_view()),
]
