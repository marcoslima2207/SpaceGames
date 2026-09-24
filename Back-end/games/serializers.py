from rest_framework import serializers
from .models import Jogo, Cliente, Venda, Avaliacao


class JogoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.SerializerMethodField()
    imagem_url_publica = serializers.SerializerMethodField()

    def get_categoria_nome(self, obj):
        return obj.categoria.nome if obj.categoria else None

    def get_imagem_url_publica(self, obj):
        imagem = obj.get_imagem_url()
        request = self.context.get('request')
        if request and imagem.startswith('/'):
            return request.build_absolute_uri(imagem)
        return imagem

    class Meta:
        model = Jogo
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Avaliacao
        fields = ['id', 'jogo', 'usuario', 'usuario_nome', 'nota', 'comentario', 'data_criacao']
        read_only_fields = ['usuario']