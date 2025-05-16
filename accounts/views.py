from django.contrib.auth import (  # biblioteca para autenticação de login
    authenticate,
    login,
    logout,
)
from django.contrib.auth.forms import (  # biblioteca para criar formulario
    AuthenticationForm,
    UserCreationForm,
)
from django.shortcuts import redirect, render

# Create your views here.


def register_view(request):
    if request.method == 'POST':   # verifica se o motodo de envio e POST
        user_form = UserCreationForm(
            request.POST
        )   # cria o formulário dentro de uma variavel que sera invocada no html
        if user_form.is_valid():   # verifica se o formulário e valido
            user_form.save()   # salva o formulário no banco de dados
            return redirect(
                'login'
            )   # apos enviar o formulário redireciona para o login
    else:   # se o metodo não for POST
        user_form = UserCreationForm()   # continua criando um formulario vazio
    return render(
        request, 'register.html', {'user_form': user_form}
    )   # envia o formulario para o html


def login_view(request):
    if request.method == 'POST':   # verifica se o usuario esta enviando algo
        username = request.POST['username']   # pega o nome de usuario digitado
        password = request.POST['password']   # pega a senha digitada
        user = authenticate(
            request, username=username, password=password
        )   # verifica se a autenticação é valida
        if user is not None:   # verifica se o usuario existe
            login(request, user)   # loga o usuario
            return redirect(
                'cars_list'
            )   # redireciona para a lista de carros ja logado
        else:
            login_form = AuthenticationForm()   # cria um formulario vazio
    else:
        login_form = AuthenticationForm()   # cria um formulario vazio
    return render(
        request, 'login.html', {'login_form': login_form}
    )  # envia o formulario para o html


def logout_view(request):
    logout(request)   # ao chamar a função ela desloga o usuario atual
    return redirect('cars_list')
