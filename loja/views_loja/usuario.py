from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render


def login_user(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        
        return render(request, 'login.html', { 'error': 'Usuário não encontrado' })
    except Exception:
        return render(request, 'login.html', { 'error': 'Ocorreu um erro interno no servidor' })
