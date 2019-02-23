from django.urls import path, include
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name="home.html"), name="home")
    path('devices/', views.DeviceList.as_view(), name='device-list'),
    path('devices/<int:pk>/', views.DeviceDetail.as_view(), name='device-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('', views.api_root),
]
