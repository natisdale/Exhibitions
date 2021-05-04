from django.urls import path
from myapp import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('exhibitions/', views.getExhibitions),
    path('exhibition/create', views.createExhibition, name='create_exhibition'),
    path('exhibition/view/<int:pk>', views.viewExhibition, name='view_exhibition'),
    path('exhibition/edit/<int:pk>', views.updateExhibition, name='edit_exhibition'),
    path('exhibition/delete/<int:pk>', views.deleteExhibition, name='delete_exhibition'),
    path('artwork/create/<int:pk>', views.createArtWork, name='create_artwork'),
    path('artwork/update/<int:pk>', views.updateArtWork, name='update_artwork'),
    path('artwork/delete/<int:pk>', views.deleteArtWork, name='delete_artwork'),
    path('mentor/create', views.createMentor, name='create_mentor'),
    path('category/create', views.createCategory, name='create_category'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('search', views.filter, name='search'),
    path('degrees', views.degreePieChart, name='degrees-chart'),
    path('years', views.yearsBarChart, name='years-chart'),
    path('categories', views.categoryChart, name='categories-chart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)