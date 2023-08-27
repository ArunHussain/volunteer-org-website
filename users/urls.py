from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
	#the 2 auth_views.[] are already defined by Django and are imported in.
    path('login/',
    	auth_views.LoginView.as_view(template_name='users/login.html'),
    	name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/',views.register, name='register'),
    #The views.register view is the only one I will need to define.
]

