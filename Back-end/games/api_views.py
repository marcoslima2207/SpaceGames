from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Jogo, Cliente, Venda, Carrinho, Favorito, Biblioteca, Avaliacao
from .serializers import (
    JogoSerializer,
    ClienteSerializer,
    VendaSerializer,
    AvaliacaoSerializer,
)

from .permissions import (
    IsAdmin,
    IsFuncionarioOuAdmin
)


class JogoViewSet(viewsets.ModelViewSet):
    queryset = Jogo.objects.all()
    serializer_class = JogoSerializer
    permission_classes = [AllowAny]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsFuncionarioOuAdmin]


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    permission_classes = [IsAdmin]


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    username = request.data.get('username', '').strip()
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '')
    first_name = request.data.get('first_name', '').strip()

    if not username or not email or not password:
        return Response({'detail': 'Preencha usuário, e-mail e senha.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Este usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
    refresh = RefreshToken.for_user(user)
    return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_summary(request):
    favorite_games = Jogo.objects.filter(favoritos__usuario=request.user).distinct()
    library_games = Jogo.objects.filter(biblioteca__usuario=request.user).distinct()
    cart_items = Carrinho.objects.filter(usuario=request.user).select_related('jogo')
    return Response({
        'user': {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'date_joined': request.user.date_joined,
        },
        'favoritos': JogoSerializer(favorite_games, many=True, context={'request': request}).data,
        'biblioteca': JogoSerializer(library_games, many=True, context={'request': request}).data,
        'carrinho': [{
            'id': item.id,
            'jogo': JogoSerializer(item.jogo, context={'request': request}).data,
            'quantidade': item.quantidade,
            'subtotal': item.get_subtotal(),
        } for item in cart_items],
    })


def _auth_game_response(request, message):
    return Response({'detail': message, 'account': account_summary(request).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite_api(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    favorite, created = Favorito.objects.get_or_create(usuario=request.user, jogo=jogo)
    if not created:
        favorite.delete()
    return _auth_game_response(request, 'Jogo favoritado.' if created else 'Jogo removido dos favoritos.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart_api(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    if Biblioteca.objects.filter(usuario=request.user, jogo=jogo).exists():
        return Response({'detail': 'Você já possui este jogo na biblioteca.'}, status=status.HTTP_400_BAD_REQUEST)
    Carrinho.objects.get_or_create(usuario=request.user, jogo=jogo, defaults={'quantidade': 1})
    return _auth_game_response(request, 'Jogo adicionado ao carrinho.')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_api(request, item_id):
    item = get_object_or_404(Carrinho, id=item_id, usuario=request.user)
    item.delete()
    return _auth_game_response(request, 'Item removido do carrinho.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_free_game_api(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id, gratuito=True)
    Biblioteca.objects.get_or_create(usuario=request.user, jogo=jogo, defaults={'preco_pago': 0})
    return _auth_game_response(request, 'Jogo gratuito adicionado à biblioteca.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_api(request):
    items = Carrinho.objects.filter(usuario=request.user).select_related('jogo')
    if not items.exists():
        return Response({'detail': 'Seu carrinho está vazio.'}, status=status.HTTP_400_BAD_REQUEST)
    for item in items:
        Biblioteca.objects.get_or_create(usuario=request.user, jogo=item.jogo, defaults={'preco_pago': item.jogo.preco})
    items.delete()
    return _auth_game_response(request, 'Compra finalizada com sucesso.')


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def reviews_api(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    if request.method == 'GET':
        reviews = Avaliacao.objects.filter(jogo=jogo).select_related('usuario')
        return Response(AvaliacaoSerializer(reviews, many=True).data)
    if not request.user.is_authenticated:
        return Response({'detail': 'Faça login para avaliar este jogo.'}, status=status.HTTP_401_UNAUTHORIZED)
    nota = request.data.get('nota')
    if not isinstance(nota, int) or nota < 1 or nota > 5:
        return Response({'detail': 'A nota deve estar entre 1 e 5.'}, status=status.HTTP_400_BAD_REQUEST)
    review, _ = Avaliacao.objects.update_or_create(
        usuario=request.user, jogo=jogo,
        defaults={'nota': nota, 'comentario': request.data.get('comentario', '')}
    )
    return Response(AvaliacaoSerializer(review).data, status=status.HTTP_201_CREATED)