from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .forms import PermisoForm
from .models import Asistencia, Empleado

@login_required
def dashboard(request):
    try:
        empleado = request.user.empleado
    except Empleado.DoesNotExist:
        return render(request, 'error.html', {'msg': 'No tienes un perfil de empleado asignado.'})
    
    asistencia_hoy = Asistencia.objects.filter(empleado=empleado, fecha=timezone.now().date()).first()
    return render(request, 'dashboard.html', {'asistencia': asistencia_hoy})

@login_required
def marcar_asistencia(request):
    empleado = request.user.empleado
    asistencia, created = Asistencia.objects.get_or_create(empleado=empleado, fecha=timezone.now().date())
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'entrada' and not asistencia.hora_entrada:
            asistencia.hora_entrada = timezone.now()
            asistencia.save()
        elif accion == 'salida' and asistencia.hora_entrada and not asistencia.hora_salida:
            asistencia.hora_salida = timezone.now()
            asistencia.save()
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def solicitar_permiso(request):
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.empleado = request.user.empleado
            permiso.save()
            return redirect('dashboard')
    else:
        form = PermisoForm()
    return render(request, 'permiso_form.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')