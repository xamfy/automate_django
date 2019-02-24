from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from main import views
from .models import Device
from .views import DeviceListView

urlpatterns = [
    path('', DeviceListView.as_view(), name="home"),
    path('devices/', views.DeviceList.as_view(), name='device-list'),
    path('devices/<int:pk>/', views.DeviceDetail.as_view(), name='device-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('api/', views.api_root),
]
