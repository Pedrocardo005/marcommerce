from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db.utils import IntegrityError


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
    if request.method == 'GET':
        return render(request, 'loja/usuario/signup.html')

    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username, email, password)

            user.save()

            data = {
                'usename': user.username,
                'email': user.email
            }

            return JsonResponse(data, status=200)
        except IntegrityError as error:
            message = str(error)
            return JsonResponse({'message': message}, status=409)

        except Exception as error:
            return JsonResponse({'message': 'Ocorreu um erro interno no servidor'}, status=500)
