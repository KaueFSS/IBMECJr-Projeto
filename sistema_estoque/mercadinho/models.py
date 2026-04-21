from django.core.validators import MinValueValidator
from django.db import models


class FormaPagamento(models.TextChoices):
    DINHEIRO = "dinheiro", "Dinheiro"
    PIX = "pix", "Pix"
    CARTAO_DEBITO = "cartao_debito", "Cartao debito"
    CARTAO_CREDITO = "cartao_credito", "Cartao credito"
    FIADO = "fiado", "Fiado"


class Fornecedor(models.Model):
    id_fornecedor = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID do fornecedor",
    )
    razao_social = models.CharField(
        max_length=150,
        verbose_name="Razao social",
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
    )
    inscricao_est = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Inscricao estadual",
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
    )
    numero = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Numero",
    )
    representante = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Representante",
    )
    rua = models.CharField(
        max_length=150,
        verbose_name="Rua",
    )
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP",
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade",
    )
    uf = models.CharField(
        max_length=2,
        verbose_name="UF",
    )

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["razao_social"]

    def __str__(self):
        return f"{self.id_fornecedor} - {self.razao_social}"


class Funcionario(models.Model):
    id_funcionario = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID do funcionario",
    )
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome",
    )
    cargo = models.CharField(
        max_length=100,
        verbose_name="Cargo",
    )
    data_admissao = models.DateField(
        verbose_name="Data de admissao",
    )
    turno = models.CharField(
        max_length=30,
        verbose_name="Turno",
    )
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Salario",
    )
    horas_semanais = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Horas semanais",
    )

    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.id_funcionario} - {self.nome}"


class Cliente(models.Model):
    id_cliente = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID do cliente",
    )
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome",
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
    )
    possui_fiado = models.BooleanField(
        default=False,
        verbose_name="Possui fiado",
    )
    saldo_fiado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Saldo fiado",
    )
    data_cadastro = models.DateField(
        verbose_name="Data de cadastro",
    )
    qtd_comprada = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade comprada",
    )
    total_valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total em compras",
    )
    bairro = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Bairro",
    )
    ultima_compra = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ultima compra",
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.id_cliente} - {self.nome}"


class Produto(models.Model):
    id_produto = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID do produto",
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name="produtos",
        db_column="id_fornecedor",
        verbose_name="Fornecedor",
    )
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome",
    )
    categoria = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Categoria",
    )
    unidade = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Unidade",
    )
    quantidade = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade em estoque",
    )
    ncm = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="NCM",
    )
    cst = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="CST",
    )
    codigo_barras = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Codigo de barras",
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preco",
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.id_produto} - {self.nome}"


