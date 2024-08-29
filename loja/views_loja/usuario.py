from django.contrib.auth import authenticate, login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render


def login_user(request: WSGIRequest):
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                return redirect('index')
            return render(request, 'login.html')

        elif request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')

            return render(request, 'login.html', {'error': 'Usuário não encontrado'})
    except Exception:
        return render(request, 'login.html', {'error': 'Ocorreu um erro interno no servidor'}, status=500)


def logout_user(request: WSGIRequest):
    logout(request)
    return render(request, 'loja/usuario/logout.html')


def create_user(request: WSGIRequest):
    pass
