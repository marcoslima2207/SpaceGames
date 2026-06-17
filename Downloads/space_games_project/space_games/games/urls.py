"""
Space_Games - URLs do app games
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Página Inicial ──────────────────────
    path('', views.home, name='home'),
    path('jogo/<int:jogo_id>/', views.detalhe_jogo, name='detalhe_jogo'),
    path('pesquisa/', views.pesquisa_view, name='pesquisa'),

    # ── Autenticação ─────────────────────────
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),

    # ── Favoritos ────────────────────────────
    path('favoritos/', views.favoritos_view, name='favoritos'),
    path('favoritos/toggle/<int:jogo_id>/', views.toggle_favorito, name='toggle_favorito'),

    # ── Carrinho ─────────────────────────────
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('carrinho/adicionar/<int:jogo_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:item_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),

    # ── Biblioteca ───────────────────────────
    path('biblioteca/', views.biblioteca_view, name='biblioteca'),
    path('biblioteca/adicionar-gratuito/<int:jogo_id>/', views.adicionar_gratuito, name='adicionar_gratuito'),

    # ── Clientes ─────────────────────────────
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
]