"""
Space_Games - URLs do app games
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página Inicial
    path('', views.home, name='home'),

    # Jogos
    path('jogo/<int:jogo_id>/', views.detalhe_jogo, name='detalhe_jogo'),
    path('download/<int:jogo_id>/', views.download_jogo, name='download_jogo'),
    path('pesquisa/', views.pesquisa_view, name='pesquisa'),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),

    # Recuperação de Senha
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='games/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='games/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='games/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='games/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Favoritos
    path('favoritos/', views.favoritos_view, name='favoritos'),
    path(
        'favoritos/toggle/<int:jogo_id>/',
        views.toggle_favorito,
        name='toggle_favorito'
    ),

    # Carrinho
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path(
        'carrinho/adicionar/<int:jogo_id>/',
        views.adicionar_carrinho,
        name='adicionar_carrinho'
    ),
    path(
        'carrinho/remover/<int:item_id>/',
        views.remover_carrinho,
        name='remover_carrinho'
    ),
    path(
        'carrinho/finalizar/',
        views.finalizar_compra,
        name='finalizar_compra'
    ),

    # Biblioteca
    path(
        'biblioteca/',
        views.biblioteca_view,
        name='biblioteca'
    ),
    path(
        'biblioteca/adicionar-gratuito/<int:jogo_id>/',
        views.adicionar_gratuito,
        name='adicionar_gratuito'
    ),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
]