from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]