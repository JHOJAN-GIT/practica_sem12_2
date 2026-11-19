from django.contrib import admin
from django.urls import path
from gestion_medica import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.agendar_cita, name='agendar_cita'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]