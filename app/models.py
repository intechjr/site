from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class Instituic(models.Model):
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return self.razao_social

class InstituicUnidade(models.Model):
    instituicao = models.ForeignKey(Instituic, related_name='unidades', on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return self.razao_social

class SectorSuper(models.Model):
    nome_super_setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_super_setor

class Sector(models.Model):
    super_setor = models.ForeignKey(SectorSuper, related_name='setores', on_delete=models.CASCADE)
    nome_setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_setor

class Subsector(models.Model):
    setor = models.ForeignKey(Sector, related_name='sub_setores', on_delete=models.CASCADE)
    nome_sub_setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_sub_setor

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_categoria

class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='sub_categorias', on_delete=models.CASCADE)
    nome_subcategoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_subcategoria

class Transaction(models.Model):
    TRANSFERENCIA = 'Doação'
    TRANSFERENCIA2 = 'Perda'
    TRANSFERENCIA3 = 'Transferência'
    TRANSFERENCIA4 = 'Entrada'
    TRANSFERENCIA5 = 'Saída'
    TIPO_CHOICES = [
        (TRANSFERENCIA, 'Doação'),
        (TRANSFERENCIA2, 'Perda'),
        (TRANSFERENCIA3, 'Transferência'),
        (TRANSFERENCIA4, 'Entrada'),
        (TRANSFERENCIA5, 'Saída'),
    ]

    transacao = models.CharField(max_length=100, choices=TIPO_CHOICES)

    def __str__(self):
        return self.transacao

class UnidadeMedida(models.Model):
    unidade_medida = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)

    def __str__(self):
        return self.unidade_medida

class Tipo(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo

class Subtipo(models.Model):
    tipo = models.ForeignKey(Tipo, related_name='subtipos', on_delete=models.CASCADE)
    subtipo = models.CharField(max_length=100)

    def __str__(self):
        return self.subtipo

class Fabricante(models.Model):
    nome_fabricante = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_fabricante

class Modelo(models.Model):
    nome_modelo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_modelo

class Marca(models.Model):
    nome_marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_marca

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, related_name='produtos', on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, related_name='produtos', on_delete=models.CASCADE)
    fabricante = models.ForeignKey(Fabricante, related_name='produtos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_produto

class TipoEmbalagem(models.Model):
    nome_embalagem = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_embalagem

class DetalheProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='detalhes', on_delete=models.CASCADE)
    unidade_produto = models.IntegerField(default=0)
    cor_produto = models.CharField(max_length=100)
    sabor_produto = models.CharField(max_length=100)
    quantidade_embalagem_produto = models.IntegerField(default=0)
    tipo_embalagem_produto = models.ForeignKey(TipoEmbalagem, related_name='produtos', on_delete=models.CASCADE)        
    preco_custo_produto = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda_produto = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.produto.nome_produto}"
    
class DetalheProdutoEstoque(models.Model):
    id_produto = models.ForeignKey(DetalheProduto, related_name= "detalhess", on_delete= models.CASCADE);  
    id_subsector = models.ForeignKey(Subsector, related_name='subsetor', on_delete=models.CASCADE)
    quantidade_estoque = models.IntegerField(default = 0);    
    def __str__(self):
        return f"{self.id_produto.produto.nome_produto} - {self.id_subsector.nome_sub_setor}"

    

class DetalheProdutoFoto(models.Model):
    id_produto = models.ForeignKey(DetalheProduto, related_name="id_det", on_delete=models.CASCADE)
    linkCaminho = models.CharField(max_length=100)
    
    def __str__(self):
        return self.id_produto.produto.nome_produto

class MovimentacaoProduto(models.Model):
    data_hora_movimentacao = models.DateTimeField(default=timezone.now)
    subsector_origem = models.ForeignKey(Subsector, related_name='movimentacoes_origem', on_delete=models.CASCADE)
    subsector_destino = models.ForeignKey(Subsector, related_name='movimentacoes_destino', on_delete=models.CASCADE)
    detalhe_produto = models.ForeignKey(DetalheProduto, related_name='movimentacoes', on_delete=models.CASCADE)
    quantidade_movimentada = models.IntegerField()
    transacao = models.ForeignKey(Transaction, related_name='movimentacoes', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Verificar estoque na origem
        try:
            estoque_origem = DetalheProdutoEstoque.objects.get(
                id_produto=self.detalhe_produto,
                id_subsector=self.subsector_origem
            )
        except DetalheProdutoEstoque.DoesNotExist:
            raise ValidationError("Produto não encontrado no estoque de origem.")

        if estoque_origem.quantidade_estoque < self.quantidade_movimentada:
            raise ValidationError("Quantidade insuficiente no estoque de origem.")

        # Atualizar estoque de origem
        estoque_origem.quantidade_estoque -= self.quantidade_movimentada
        estoque_origem.save()

        # Verificar ou criar estoque no subsetor de destino
        estoque_destino, created = DetalheProdutoEstoque.objects.get_or_create(
            id_produto=self.detalhe_produto,
            id_subsector=self.subsector_destino
        )
        estoque_destino.quantidade_estoque += self.quantidade_movimentada
        estoque_destino.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Movimentação de {self.quantidade_movimentada} unidades de {self.detalhe_produto.produto.nome_produto} entre {self.subsector_origem.nome_sub_setor} e {self.subsector_destino.nome_sub_setor}"

class ProdutoMovimentoItem(models.Model):
    id_produto_saida = models.ForeignKey('DetalheProduto', related_name='produtos_saida', on_delete=models.CASCADE)
    id_produto = models.ForeignKey('DetalheProduto', related_name='produtos', on_delete=models.CASCADE)
    qtde = models.IntegerField()
    preco_saida = models.DecimalField(max_digits=10, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id_produto_saida.produto.nome_produto} -> {self.id_produto.produto.nome_produto}"
    
class CustomUser(AbstractUser):
    subsetor = models.ForeignKey(Subsector, on_delete=models.SET_NULL, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_user')
    preferred_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.preferred_name
    




