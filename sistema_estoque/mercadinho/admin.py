from django.contrib import admin
from .models import (
    Cliente,
    Fornecedor,
    Funcionario,
    Produto,
    CompraFornecedor,
    Despesa,
    Estoque,
    Venda,
    ItemCompra,
    ItemVenda,
)

admin.site.register(Cliente)
admin.site.register(Fornecedor)
admin.site.register(Funcionario)
admin.site.register(Produto)
admin.site.register(CompraFornecedor)
admin.site.register(Despesa)
admin.site.register(Estoque)
admin.site.register(Venda)
admin.site.register(ItemCompra)
admin.site.register(ItemVenda)