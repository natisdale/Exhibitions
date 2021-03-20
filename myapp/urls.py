from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view),
    path('register/', views.register, name='register'),
]