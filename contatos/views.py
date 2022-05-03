from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Contato


def index(request):
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    contatos = paginator.get_page(page_number)
    return render(request, 'contatos/pages/index.html', {
        'contatos': contatos,
    })


def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:   # evita forçar páginas de número não permitidas mostrar  # noqa E501
        raise Http404()

    return render(request, 'contatos/pages/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')
    if termo is None or not termo:
        messages.add_message(
            request,
            messages.ERROR,
            'Campo termo não pode ficar vazio.'
        )
        return redirect('contatos:index')
    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
     ).filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 15)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    contatos = paginator.get_page(page_number)
    return render(request, 'contatos/pages/busca.html', {
        'contatos': contatos,
    })


def deleta_contato(request, contato_id):
    contato_apagar = Contato.objects.get(id=contato_id)
    nome = contato_apagar.nome
    contato_apagar.delete()
    messages.add_message(
            request,
            messages.SUCCESS,
            'Contato: ' + nome + ' apagado com sucesso!'
        )
    return redirect('contatos:index')
