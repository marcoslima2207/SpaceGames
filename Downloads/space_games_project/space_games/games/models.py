"""
Space_Games - Models do Django
Define todas as tabelas do banco de dados usando Django ORM
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    def __str__(self):
        return self.nome

class Categoria(models.Model):
    
    """Categorias de jogos (Ação, RPG, Esporte, etc.)"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    icone = models.CharField(
        max_length=50, blank=True, default='🎮',
        verbose_name='Ícone (emoji)'
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Gera slug automaticamente a partir do nome
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Jogo(models.Model):
    """Tabela principal de jogos"""
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    preco = models.DecimalField(
        max_digits=8, decimal_places=2,
        default=0.00, verbose_name='Preço (R$)'
    )
    gratuito = models.BooleanField(
        default=False, verbose_name='Gratuito'
    )
    destaque = models.BooleanField(
        default=False, verbose_name='Em Destaque'
    )
    imagem = models.ImageField(
        upload_to='jogos/', blank=True, null=True,
        verbose_name='Imagem de Capa'
    )
    imagem_url = models.URLField(
        blank=True, null=True,
        verbose_name='URL da Imagem (alternativa)'
    )
    arquivo_instalacao = models.FileField(
    upload_to='downloads/',
    blank=True,
    null=True,
    verbose_name='Arquivo para Download'
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='jogos', verbose_name='Categoria'
    )
    desenvolvedor = models.CharField(
        max_length=200, blank=True, verbose_name='Desenvolvedor'
    )
    ano_lancamento = models.IntegerField(
        null=True, blank=True, verbose_name='Ano de Lançamento'
    )
    avaliacao = models.DecimalField(
        max_digits=3, decimal_places=1,
        default=0.0, verbose_name='Avaliação (0-5)'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação'
    )
    estoque = models.PositiveIntegerField(
        default=0
    )
    estoque_minimo = models.PositiveIntegerField(
        default=5
    )
    class Meta:
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

    def get_imagem_url(self):
        """Retorna URL da imagem (arquivo ou URL externa)"""
        if self.imagem:
            return self.imagem.url
        if self.imagem_url:
            return self.imagem_url
        return '/static/img/default_game.png'

    def get_preco_display(self):
        """Retorna preço formatado"""
        if self.gratuito:
            return 'Grátis'
        return f'R$ {self.preco:.2f}'.replace('.', ',')


class Favorito(models.Model):
    """Tabela de jogos favoritos por usuário"""
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favoritos', verbose_name='Usuário'
    )
    jogo = models.ForeignKey(
        Jogo, on_delete=models.CASCADE,
        related_name='favoritos', verbose_name='Jogo'
    )
    data_adicionado = models.DateTimeField(
        auto_now_add=True, verbose_name='Data Adicionado'
    )

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        # Garante que um usuário não pode favoritar o mesmo jogo duas vezes
        unique_together = ['usuario', 'jogo']
        ordering = ['-data_adicionado']

    def __str__(self):
        return f'{self.usuario.username} → {self.jogo.titulo}'


class Carrinho(models.Model):
    """Tabela do carrinho de compras"""
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='carrinho', verbose_name='Usuário'
    )
    jogo = models.ForeignKey(
        Jogo, on_delete=models.CASCADE,
        related_name='carrinho', verbose_name='Jogo'
    )
    quantidade = models.PositiveIntegerField(
        default=1, verbose_name='Quantidade'
    )
    data_adicionado = models.DateTimeField(
        auto_now_add=True, verbose_name='Data Adicionado'
    )

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = ['usuario', 'jogo']
        ordering = ['-data_adicionado']

    def __str__(self):
        return f'Carrinho de {self.usuario.username}: {self.jogo.titulo}'

    def get_subtotal(self):
        """Calcula subtotal do item"""
        return self.jogo.preco * self.quantidade


class Biblioteca(models.Model):
    """Tabela da biblioteca de jogos comprados/adquiridos"""
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='biblioteca', verbose_name='Usuário'
    )
    jogo = models.ForeignKey(
        Jogo, on_delete=models.CASCADE,
        related_name='biblioteca', verbose_name='Jogo'
    )
    data_compra = models.DateTimeField(
        default=timezone.now, verbose_name='Data da Compra'
    )
    preco_pago = models.DecimalField(
        max_digits=8, decimal_places=2,
        default=0.00, verbose_name='Preço Pago'
    )

    class Meta:
        verbose_name = 'Jogo na Biblioteca'
        verbose_name_plural = 'Jogos na Biblioteca'
        unique_together = ['usuario', 'jogo']
        ordering = ['-data_compra']

    def __str__(self):
        return f'Biblioteca de {self.usuario.username}: {self.jogo.titulo}'

class Venda(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Venda #{self.id}"

class ItemVenda(models.Model):

    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE
    )

    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.PROTECT
    )

    quantidade = models.PositiveIntegerField()

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):

        # venda nova
        if not self.pk:

            if self.jogo.estoque < self.quantidade:
                raise ValueError(
                    f'Estoque insuficiente para {self.jogo.titulo}'
                )

            self.jogo.estoque -= self.quantidade
            self.jogo.save()

        super().save(*args, **kwargs)

        total = 0

        for item in self.venda.itemvenda_set.all():
            total += (
                item.preco_unitario *
                item.quantidade
            )

        self.venda.valor_total = total
        self.venda.save()

    def __str__(self):
        return f'{self.jogo.titulo} ({self.quantidade})'
    
class Perfil(models.Model):

    TIPOS = [
        ('ADMIN', 'Administrador'),
        ('FUNCIONARIO', 'Funcionário'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='FUNCIONARIO'
    )

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo}'