from django.urls import path

from .views import Index
from points import views


# app_name = 'points'

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('hub/', views.UserHub, name='hub'),
	path('send/', views.send_points, name='send'),
	path('redeem/', views.redeem_points, name='redeem'),
	path('userhistory/', views.user_history, name='userhistory'),
	path('reset/', views.reset_points, name='reset'),
	path('redemptionReport/', views.redemption_report, name='redemptionReport'),
]