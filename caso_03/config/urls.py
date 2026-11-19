from django.contrib import admin
from django.urls import path
from control_rrhh import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('asistencia/', views.marcar_asistencia, name='marcar_asistencia'),
    path('permiso/', views.solicitar_permiso, name='solicitar_permiso'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]