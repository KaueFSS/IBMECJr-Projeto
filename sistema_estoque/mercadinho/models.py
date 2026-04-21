from django.db import models

## Vou usar isso aqui depois - (Kauê)
FORMAS_PAGAMENTO = [
    ('dinheiro', 'Dinheiro', 'DINHEIRO', 'dinheiro', 'Especie', 'Espécie'),
    ('pix', 'PIX', 'PIX ', 'Pix', 'pix'),
    ('cartao_debito', 'Cartão Débito', 'Cartão Débito', 'Cartao_Debito', 'Debito', 'cartao_debito'),
    ('cartao_credito', 'Cartão Crédito', 'Cartão Crédito', 'Cartao_Credito', 'Credito', 'cartao_credito'),
    ('fiado', 'Fiado', 'FIADO', 'fiado'),
]


class Venda(models.Model):
 

    id_venda = models.CharField(
        max_length=10,
        verbose_name="ID da Venda"
    )
    data_venda = models.DateField(
        verbose_name="Data da Venda"
    )
    hora = models.TimeField(
        verbose_name="Hora da Venda"
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMAS_PAGAMENTO,
        verbose_name="Forma de Pagamento"
    )
    id_funcionario = models.CharField(
        max_length=10,
        verbose_name="ID do Funcionário"
    )
    id_cliente = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="ID do Cliente"
    )
 
    # --- Item da venda ---
    id_produto = models.CharField(
        max_length=10,
        verbose_name="ID do Produto"
    )
    nome_produto = models.CharField(
        max_length=200,
        verbose_name="Nome do Produto"
    )
    quantidade = models.IntegerField(
        verbose_name="Quantidade"
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário (R$)"
    )
    desconto_aplicado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Desconto Aplicado (%)"
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Subtotal (R$)"
    )
 
    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-data_venda', '-hora']
 
    def __str__(self):
        return f"Venda {self.id_venda} — {self.nome_produto} (x{self.quantidade})"