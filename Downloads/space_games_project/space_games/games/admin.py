"""
Space_Games - Configuração do Django Admin
"""

from django.contrib import admin
from .models import Categoria, Jogo, Favorito, Carrinho, Biblioteca

from django.contrib import admin
from .models import Cliente, Venda, ItemVenda
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo']
    list_filter = ['tipo']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'telefone']
    search_fields = ['nome', 'cpf', 'email']
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'usuario', 'valor_total', 'data']
    list_filter = ['data']
    search_fields = ['cliente__nome']

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = [
        'venda',
        'jogo',
        'quantidade',
        'preco_unitario'
    ]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'slug', 'total_jogos']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome']

    def total_jogos(self, obj):
        return obj.jogos.count()
    total_jogos.short_description = 'Total de Jogos'


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'categoria', 'preco', 'gratuito',
        'destaque', 'avaliacao', 'data_criacao'
    ]
    list_filter = ['gratuito', 'destaque', 'categoria']
    search_fields = ['titulo', 'descricao', 'desenvolvedor']
    list_editable = ['gratuito', 'destaque', 'preco']
    readonly_fields = ['data_criacao']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'categoria', 'desenvolvedor', 'ano_lancamento')
        }),
        ('Preço e Disponibilidade', {
            'fields': ('preco', 'gratuito', 'destaque')
        }),
       ('Mídia', {
        'fields': (
        'imagem',
        'imagem_url',
        'arquivo_instalacao'
        )
        }),
        ('Avaliação', {
            'fields': ('avaliacao',)
        }),
        ('Datas', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'jogo', 'data_adicionado']
    list_filter = ['data_adicionado']
    search_fields = ['usuario__username', 'jogo__titulo']
    raw_id_fields = ['usuario', 'jogo']


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'jogo', 'quantidade', 'data_adicionado']
    list_filter = ['data_adicionado']
    search_fields = ['usuario__username', 'jogo__titulo']


@admin.register(Biblioteca)
class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'jogo', 'preco_pago', 'data_compra']
    list_filter = ['data_compra']
    search_fields = ['usuario__username', 'jogo__titulo']
    readonly_fields = ['data_compra']
