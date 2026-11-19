from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import PrestamoForm
from .models import Prestamo

@login_required
def solicitar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST, user=request.user)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.docente = request.user
            prestamo.save()
            return redirect('mis_prestamos')
    else:
        form = PrestamoForm(user=request.user)
    return render(request, 'prestamo_form.html', {'form': form})

@login_required
def mis_prestamos(request):
    # Docentes solo ven sus propios préstamos
    prestamos = Prestamo.objects.filter(docente=request.user)
    return render(request, 'mis_prestamos.html', {'prestamos': prestamos})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('solicitar_prestamo')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')