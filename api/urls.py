from django.urls import path, include

from . import views

urlpatterns = [
    path('sync/', views.sync),
    path('traffic/', views.traffic),
    path('sync_ss/', views.sync_ss),
    path('traffic_ss/', views.traffic_ss),
]
