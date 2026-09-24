from rest_framework.routers import DefaultRouter
from django.urls import path
from .api_views import (
	JogoViewSet, ClienteViewSet, VendaViewSet, register_api, account_summary,
	toggle_favorite_api, add_cart_api, remove_cart_api, add_free_game_api,
	checkout_api,
	reviews_api,
)

router = DefaultRouter()

router.register(r'jogos', JogoViewSet, basename='jogos')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'vendas', VendaViewSet, basename='vendas')

urlpatterns = router.urls
urlpatterns += [
	path('auth/register/', register_api, name='api_register'),
	path('auth/me/', account_summary, name='account_summary'),
	path('jogos/<int:jogo_id>/favorito/', toggle_favorite_api, name='toggle_favorite_api'),
	path('jogos/<int:jogo_id>/carrinho/', add_cart_api, name='add_cart_api'),
	path('carrinho/<int:item_id>/', remove_cart_api, name='remove_cart_api'),
	path('jogos/<int:jogo_id>/gratuito/', add_free_game_api, name='add_free_game_api'),
	path('carrinho/finalizar/', checkout_api, name='checkout_api'),
	path('jogos/<int:jogo_id>/avaliacoes/', reviews_api, name='reviews_api'),
]