"""
Space_Games - Context Processors
Disponibiliza dados globais para todos os templates
"""

from .models import Carrinho


def carrinho_count(request):
    """
    Adiciona a contagem de itens no carrinho ao contexto global.
    Disponível em todos os templates como {{ carrinho_count }}
    """
    count = 0
    if request.user.is_authenticated:
        count = Carrinho.objects.filter(usuario=request.user).count()
    return {'carrinho_count': count}
