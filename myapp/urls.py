from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
]