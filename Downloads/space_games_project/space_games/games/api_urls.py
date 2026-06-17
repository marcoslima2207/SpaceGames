from django.urls import path
from .api_views import (JogoViewSet, ClienteViewSet, VendaViewSet
)

jogos_list = JogoViewSet.as_view({
    'get': 'list',
})

clientes_list = ClienteViewSet.as_view({
    'get': 'list',
})

vendas_list = VendaViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('jogos/', jogos_list, name='api_jogos'),
    path('clientes/', clientes_list, name='api_clientes'),
    path('vendas/', vendas_list, name='api_vendas'),
]