"""
Space_Games - Views do Django
Lógica de negócio para todas as páginas e funcionalidades
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Jogo, Categoria, Favorito, Carrinho, Biblioteca, Cliente
from .forms import CadastroForm, PerfilForm


# ─────────────────────────────────────────────
# PÁGINA INICIAL
# ─────────────────────────────────────────────

def home(request):
    """
    Página inicial com jogos em destaque, categorias e jogos gratuitos.
    Suporta filtragem por categoria e pesquisa.
    """
    # Parâmetros de filtro da URL
    query = request.GET.get('q', '')
    categoria_slug = request.GET.get('categoria', '')

    # Queryset base
    jogos = Jogo.objects.select_related('categoria').all()

    # Filtro por pesquisa
    if query:
        jogos = jogos.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(desenvolvedor__icontains=query)
        )

    # Filtro por categoria
    categoria_selecionada = None
    if categoria_slug:
        categoria_selecionada = get_object_or_404(Categoria, slug=categoria_slug)
        jogos = jogos.filter(categoria=categoria_selecionada)

    # Dados para a página
    jogos_destaque = Jogo.objects.filter(destaque=True)[:6]
    jogos_gratuitos = Jogo.objects.filter(gratuito=True)[:8]
    categorias = Categoria.objects.all()

    context = {
        'jogos': jogos,
        'jogos_destaque': jogos_destaque,
        'jogos_gratuitos': jogos_gratuitos,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
        'query': query,
        'total_resultados': jogos.count() if (query or categoria_slug) else None,
    }
    return render(request, 'games/home.html', context)


def detalhe_jogo(request, jogo_id):
    """Página de detalhes de um jogo específico"""
    jogo = get_object_or_404(Jogo, id=jogo_id)

    # Verificações de estado para o usuário logado
    is_favorito = False
    no_carrinho = False
    na_biblioteca = False

    if request.user.is_authenticated:
        is_favorito = Favorito.objects.filter(
            usuario=request.user, jogo=jogo
        ).exists()
        no_carrinho = Carrinho.objects.filter(
            usuario=request.user, jogo=jogo
        ).exists()
        na_biblioteca = Biblioteca.objects.filter(
            usuario=request.user, jogo=jogo
        ).exists()

    # Jogos relacionados (mesma categoria)
    jogos_relacionados = Jogo.objects.filter(
        categoria=jogo.categoria
    ).exclude(id=jogo.id)[:4]

    context = {
        'jogo': jogo,
        'is_favorito': is_favorito,
        'no_carrinho': no_carrinho,
        'na_biblioteca': na_biblioteca,
        'jogos_relacionados': jogos_relacionados,
    }
    return render(request, 'games/detalhe_jogo.html', context)


# ─────────────────────────────────────────────
# AUTENTICAÇÃO
# ─────────────────────────────────────────────

def login_view(request):
    """Login de usuários"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}! 🚀')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()

    return render(request, 'games/login.html', {'form': form})


def cadastro_view(request):
    """Cadastro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}! 🎮')
            return redirect('home')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CadastroForm()

    return render(request, 'games/cadastro.html', {'form': form})


def logout_view(request):
    """Logout do usuário"""
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('home')


# ─────────────────────────────────────────────
# FAVORITOS
# ─────────────────────────────────────────────

@login_required
def favoritos_view(request):
    """Lista todos os jogos favoritos do usuário"""
    favoritos = Favorito.objects.filter(
        usuario=request.user
    ).select_related('jogo', 'jogo__categoria')

    return render(request, 'games/favoritos.html', {'favoritos': favoritos})


@login_required
@require_POST
def toggle_favorito(request, jogo_id):
    """Adiciona ou remove um jogo dos favoritos (via AJAX ou redirect)"""
    jogo = get_object_or_404(Jogo, id=jogo_id)
    favorito, criado = Favorito.objects.get_or_create(
        usuario=request.user, jogo=jogo
    )

    if not criado:
        # Já era favorito — remove
        favorito.delete()
        acao = 'removido'
        mensagem = f'"{jogo.titulo}" removido dos favoritos.'
    else:
        acao = 'adicionado'
        mensagem = f'"{jogo.titulo}" adicionado aos favoritos! ⭐'

    # Responde com JSON se for requisição AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'acao': acao, 'mensagem': mensagem})

    messages.success(request, mensagem)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ─────────────────────────────────────────────
# CARRINHO
# ─────────────────────────────────────────────

@login_required
def carrinho_view(request):
    """Exibe o carrinho de compras do usuário"""
    itens = Carrinho.objects.filter(
        usuario=request.user
    ).select_related('jogo', 'jogo__categoria')

    total = sum(item.get_subtotal() for item in itens)

    return render(request, 'games/carrinho.html', {
        'itens': itens,
        'total': total,
    })


@login_required
@require_POST
def adicionar_carrinho(request, jogo_id):
    """Adiciona um jogo ao carrinho"""
    jogo = get_object_or_404(Jogo, id=jogo_id)

    # Verifica se já está na biblioteca
    if Biblioteca.objects.filter(usuario=request.user, jogo=jogo).exists():
        messages.warning(request, f'Você já possui "{jogo.titulo}" na sua biblioteca!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    item, criado = Carrinho.objects.get_or_create(
        usuario=request.user, jogo=jogo,
        defaults={'quantidade': 1}
    )

    if not criado:
        messages.info(request, f'"{jogo.titulo}" já está no seu carrinho.')
    else:
        messages.success(request, f'"{jogo.titulo}" adicionado ao carrinho! 🛒')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = Carrinho.objects.filter(usuario=request.user).count()
        return JsonResponse({'status': 'ok', 'count': count})

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@require_POST
def remover_carrinho(request, item_id):
    """Remove um item do carrinho"""
    item = get_object_or_404(Carrinho, id=item_id, usuario=request.user)
    titulo = item.jogo.titulo
    item.delete()
    messages.success(request, f'"{titulo}" removido do carrinho.')
    return redirect('carrinho')


@login_required
@require_POST
def finalizar_compra(request):
    """Finaliza a compra — move itens do carrinho para a Biblioteca"""
    itens = Carrinho.objects.filter(
        usuario=request.user
    ).select_related('jogo')

    if not itens.exists():
        messages.warning(request, 'Seu carrinho está vazio!')
        return redirect('carrinho')

    comprados = []
    for item in itens:
        # Adiciona à biblioteca (ignora se já existir)
        Biblioteca.objects.get_or_create(
            usuario=request.user,
            jogo=item.jogo,
            defaults={'preco_pago': item.jogo.preco}
        )
        comprados.append(item.jogo.titulo)

    # Limpa o carrinho
    itens.delete()

    nomes = ', '.join(comprados[:3])
    if len(comprados) > 3:
        nomes += f' e mais {len(comprados) - 3}'
    messages.success(request, f'Compra finalizada! {nomes} adicionado(s) à sua biblioteca! 🎉')
    return redirect('biblioteca')


# ─────────────────────────────────────────────
# BIBLIOTECA
# ─────────────────────────────────────────────

@login_required
def biblioteca_view(request):
    """Exibe a biblioteca de jogos do usuário"""
    jogos_biblioteca = Biblioteca.objects.filter(
        usuario=request.user
    ).select_related('jogo', 'jogo__categoria').order_by('-data_compra')

    return render(request, 'games/biblioteca.html', {
        'jogos_biblioteca': jogos_biblioteca,
    })


@login_required
@require_POST
def adicionar_gratuito(request, jogo_id):
    """Adiciona jogo gratuito direto à biblioteca"""
    jogo = get_object_or_404(Jogo, id=jogo_id, gratuito=True)

    _, criado = Biblioteca.objects.get_or_create(
        usuario=request.user,
        jogo=jogo,
        defaults={'preco_pago': 0.00}
    )

    if criado:
        messages.success(request, f'"{jogo.titulo}" adicionado à sua biblioteca gratuitamente! 🎮')
    else:
        messages.info(request, f'Você já possui "{jogo.titulo}" na sua biblioteca.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ─────────────────────────────────────────────
# PESQUISA
# ─────────────────────────────────────────────

def pesquisa_view(request):
    """Página de resultados de pesquisa"""
    query = request.GET.get('q', '').strip()
    jogos = []

    if query:
        jogos = Jogo.objects.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(desenvolvedor__icontains=query) |
            Q(categoria__nome__icontains=query)
        ).select_related('categoria').distinct()

    return render(request, 'games/pesquisa.html', {
        'jogos': jogos,
        'query': query,
        'total': len(jogos),
    })

# ─────────────────────────────────────────────
# CLIENTES
# ─────────────────────────────────────────────

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('nome')

    return render(
        request,
        'games/clientes_lista.html',
        {'clientes': clientes}
    )


@login_required
def criar_cliente(request):

    if request.method == 'POST':

        Cliente.objects.create(
            nome=request.POST.get('nome'),
            cpf=request.POST.get('cpf'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            endereco=request.POST.get('endereco')
        )

        messages.success(
            request,
            'Cliente cadastrado com sucesso!'
        )

        return redirect('lista_clientes')

    return render(
        request,
        'games/cliente_form.html'
    )