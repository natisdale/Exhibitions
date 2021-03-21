from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view),
    path('register/', views.register, name='register'),
    path('exhibitions/', views.getExhibitions),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)