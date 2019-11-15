from django.urls import path

from .views import Index, Register, Success, UserHub
from points import views


# app_name = 'points'

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('success/', Success.as_view(), name='success'),
	path('login/', views.user_login, name = 'login'),
	path('hub/', UserHub.as_view(), name='hub'),
	path('send/', views.send_points, name='send'),
	path('register/', Register.as_view(), name='register'),
	
]