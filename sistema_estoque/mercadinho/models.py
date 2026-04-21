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


class Venda(models.Model):
    id_venda = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID da venda",
    )
    data_venda = models.DateField(
        verbose_name="Data da venda",
    )
    hora = models.TimeField(
        verbose_name="Hora da venda",
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FormaPagamento.choices,
        verbose_name="Forma de pagamento",
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="vendas",
        db_column="id_funcionario",
        verbose_name="Funcionario",
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vendas",
        db_column="id_cliente",
        verbose_name="Cliente",
    )

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ["-data_venda", "-hora"]

    def __str__(self):
        return f"Venda {self.id_venda}"


class ItemVenda(models.Model):
    id_item_venda = models.AutoField(primary_key=True)
    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
        related_name="itens",
        db_column="id_venda",
        verbose_name="Venda",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="itens_venda",
        db_column="id_produto",
        verbose_name="Produto",
    )
    quantidade_vendida = models.PositiveIntegerField(
        verbose_name="Quantidade vendida",
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preco unitario",
    )
    desconto_aplicado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Desconto aplicado",
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Subtotal",
    )

    class Meta:
        verbose_name = "Item da venda"
        verbose_name_plural = "Itens da venda"
        ordering = ["venda_id", "produto_id"]

    def __str__(self):
        return f"{self.venda_id} - {self.produto.nome} x{self.quantidade_vendida}"


class CompraFornecedor(models.Model):
    id_compra = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID da compra",
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name="compras",
        db_column="id_fornecedor",
        verbose_name="Fornecedor",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="compras_fornecedor",
        db_column="id_produto",
        verbose_name="Produto",
    )
    data_compra = models.DateField(
        verbose_name="Data da compra",
    )
    cfop = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="CFOP",
    )
    quantidade = models.PositiveIntegerField(
        verbose_name="Quantidade",
    )
    status = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Status",
    )
    data_entrega = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de entrega",
    )
    nota_fiscal = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Nota fiscal",
    )
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Valor unitario",
    )
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Valor total",
    )

    class Meta:
        verbose_name = "Compra de fornecedor"
        verbose_name_plural = "Compras de fornecedor"
        ordering = ["-data_compra"]

    def __str__(self):
        return f"Compra {self.id_compra} - {self.fornecedor.razao_social}"


class Despesa(models.Model):
    id_despesa = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID da despesa",
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="despesas",
        db_column="id_funcionario",
        verbose_name="Funcionario",
    )
    compra = models.ForeignKey(
        CompraFornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="despesas",
        db_column="id_compra",
        verbose_name="Compra vinculada",
    )
    data = models.DateField(
        verbose_name="Data",
    )
    categoria = models.CharField(
        max_length=100,
        verbose_name="Categoria",
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Valor",
    )

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ["-data"]

    def __str__(self):
        return f"Despesa {self.id_despesa} - {self.categoria}"


class Estoque(models.Model):
    id_estoque = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="ID do estoque",
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="estoques",
        db_column="id_produto",
        verbose_name="Produto",
    )

    quantidade_atual = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Quantidade atual",
    )

    estoque_minimo = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Estoque mínimo",
    )

    estoque_maximo = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Estoque máximo",
    )

    data_ultima_entrada = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data da última entrada",
    )

    data_ultima_saida = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data da última saída",
    )

    local_armazenamento = models.CharField(
        max_length=100,
        verbose_name="Local de armazenamento",
    )

    status_estoque = models.CharField(
        max_length=30,
        verbose_name="Status do estoque",
    )

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
        ordering = ["id_estoque"]

    def __str__(self):
        return f"Estoque {self.id_estoque} - {self.produto.nome}"