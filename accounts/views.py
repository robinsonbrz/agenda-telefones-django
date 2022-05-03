from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from accounts.models import FormContato

# Create your views here.


def lista_login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso!')
    return redirect('accounts:lista_add_contato')


def lista_logout(request):
    auth.logout(request)
    return redirect('contatos:index')


def lista_registro(request):
    if request.method != 'POST':
        return render(request, 'accounts/registro.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if not nome or not sobrenome or not email or not usuario or not \
            senha or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio.')
        return render(request, 'accounts/registro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/registro.html')

    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter mais que 5 caracteres.')
        return render(request, 'accounts/registro.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuario precisa ter mais que 5 caracteres.')
        return render(request, 'accounts/registro.html')

    if senha != senha2:
        messages.error(request, 'Senhas digitadas precisam ser iguais.')
        return render(request, 'accounts/registro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/registro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe.')
        return render(request, 'accounts/registro.html')

    messages.success(request, 'Registrado com sucesso! Agora faça o login.')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('accounts:lista_login')
    # messages.info(request, 'Nada postado.')
    # print(request.POST)


@login_required(redirect_field_name='accounts:lista_login')
def lista_add_contato(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/add_contato.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        form = FormContato(request.POST)
        return render(request, 'accounts/add_contato.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais que 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/add_contato.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!') # noqa e501
    return redirect('accounts:lista_add_contato')
