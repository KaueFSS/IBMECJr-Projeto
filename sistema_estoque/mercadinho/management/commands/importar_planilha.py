from django.core.management.base import BaseCommand
import pandas as pd
from decimal import Decimal
from datetime import date, datetime, time as dt_time

from mercadinho.models import (
    Produto,
    Venda,
    Cliente,
    Funcionario,
    Estoque,
    Fornecedor,
    ItemCompra,
    CompraFornecedor,
    ItemVenda,
    Despesa,
    FORMAS_PAGAMENTO_ALIASES,
)


# ---------------- FUNCOES AUXILIARES ----------------

def texto_ou_vazio(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def booleano_da_planilha(valor):
    if pd.isna(valor):
        return False
    return str(valor).strip().lower() in ["sim", "s", "true", "1"]


def limpar_decimal(valor):
    texto = str(valor).replace("R$", "").replace("%", "").strip()

    if "," in texto and "." not in texto:
        texto = texto.replace(",", ".")

    elif "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")

    return Decimal(texto)


def tratar_data(valor):
    if pd.isna(valor):
        return None

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    data_tratada = pd.to_datetime(valor, dayfirst=True, errors="coerce")

    if pd.isna(data_tratada):
        return None

    return data_tratada.date()


def tratar_hora(valor):
    if pd.isna(valor):
        return None

    if isinstance(valor, datetime):
        return valor.time()

    if isinstance(valor, dt_time):
        return valor

    hora_tratada = pd.to_datetime(valor, errors="coerce")

    if pd.isna(hora_tratada):
        return None

    return hora_tratada.time()


def primeiro_valido(grupo, coluna):
    valores = grupo[coluna].dropna()
    if valores.empty:
        return None
    return valores.iloc[0]




class Command(BaseCommand):
    help = "Importa dados da planilha para o banco"

    def handle(self, *args, **kwargs):

        # ---------------- PRODUTOS ----------------
        df_produtos = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Produtos")

        for _, row in df_produtos.iterrows():
            Produto.objects.update_or_create(
                id_produto=texto_ou_vazio(row["ID_Produto"]),
                defaults={
                    "nome": texto_ou_vazio(row["Nome"]),
                    "categoria": texto_ou_vazio(row["Categoria"]),
                    "subcategoria": texto_ou_vazio(row["Subcategoria"]),
                    "marca": texto_ou_vazio(row["Marca"]),
                    "unidade": texto_ou_vazio(row["Unidade"]),
                    "codigo_barras": texto_ou_vazio(row["Cod_Barras"]),
                    "preco_custo": limpar_decimal(row["Preco_Custo"]),
                    "preco": limpar_decimal(row["Preco_Venda"]),
                },
            )

        self.stdout.write("Produtos importados")

        # ---------------- CLIENTES ----------------
        df_clientes = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Clientes")

        for _, row in df_clientes.iterrows():
            Cliente.objects.update_or_create(
                id_cliente=texto_ou_vazio(row["ID_Cliente"]),
                defaults={
                    "nome": texto_ou_vazio(row["Nome"]),
                    "telefone": texto_ou_vazio(row["Telefone"]),
                    "bairro": texto_ou_vazio(row["Bairro"]),
                    "data_cadastro": tratar_data(row["Data_Cadastro"]) or date.today(),
                    "total_valor": limpar_decimal(row["Total_Compras"]),
                    "ultima_compra": tratar_data(row["Ultima_Compra"]),
                    "possui_fiado": booleano_da_planilha(row["Possui_Fiado"]),
                    "saldo_fiado": limpar_decimal(row["Saldo_Fiado"]),
                },
            )

        self.stdout.write("Clientes importados")

        # ---------------- FORNECEDORES ----------------
        df_fornecedores = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Fornecedores")

        for _, row in df_fornecedores.iterrows():
            Fornecedor.objects.update_or_create(
                id_fornecedor=texto_ou_vazio(row["ID_Fornecedor"]),
                defaults={
                    "razao_social": texto_ou_vazio(row["Razao_Social"]),
                    "nome_fantasia": texto_ou_vazio(row["Nome_Fantasia"]),
                    "cnpj": texto_ou_vazio(row["CNPJ"]),
                    "email": texto_ou_vazio(row["Email"]),
                    "cidade": texto_ou_vazio(row["Cidade"]),
                    "uf": texto_ou_vazio(row["Estado"]),
                    "telefone": texto_ou_vazio(row["Telefone"]),
                    "prazo_de_entraga": texto_ou_vazio(row["Prazo_Entrega_Dias"]),
                    "avaliacao": limpar_decimal(row["Avaliacao"]),
                },
            )

        self.stdout.write("Fornecedores importados")

        # ---------------- FUNCIONARIOS ----------------
        df_funcionarios = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Funcionarios")

        for _, row in df_funcionarios.iterrows():
            Funcionario.objects.update_or_create(
                id_funcionario=texto_ou_vazio(row["ID_Funcionario"]),
                defaults={
                    "nome": texto_ou_vazio(row["Nome"]),
                    "cargo": texto_ou_vazio(row["Cargo"]),
                    "data_admissao": tratar_data(row["Data_Admissao"]),
                    "turno": texto_ou_vazio(row["Turno"]),
                    "salario": limpar_decimal(row["Salario"]),
                    "horas_semanais": limpar_decimal(row["Horas_Semanais"]),
                    "ativo": texto_ou_vazio(row["Status"]).lower() == "ativo",
                },
            )

        self.stdout.write("Funcionários importados")

        # ---------------- VENDAS ----------------
        df_vendas = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Vendas")

        for id_venda, grupo in df_vendas.groupby("ID_Venda"):
            id_funcionario = primeiro_valido(grupo, "ID_Funcionario")
            id_cliente = primeiro_valido(grupo, "ID_Cliente")
            data_venda = tratar_data(primeiro_valido(grupo, "Data_Venda"))
            hora_venda = tratar_hora(primeiro_valido(grupo, "Hora_Venda"))
            forma_bruta = texto_ou_vazio(primeiro_valido(grupo, "Forma_Pagamento"))
            forma_pagamento = FORMAS_PAGAMENTO_ALIASES.get(forma_bruta, forma_bruta.lower())

            if id_funcionario is None:
                self.stdout.write(
                    self.style.WARNING(f"Venda {id_venda} ignorada: sem funcionario")
                )
                continue

            if data_venda is None:
                data_venda = date(2026, 4, 24)

            Venda.objects.update_or_create(
                id_venda=texto_ou_vazio(id_venda),
                defaults={
                    "data_venda": data_venda,
                    "hora": hora_venda or dt_time(0, 0),
                    "forma_pagamento": forma_pagamento,
                    "funcionario_id": texto_ou_vazio(id_funcionario),
                    "cliente_id": None if id_cliente is None else texto_ou_vazio(id_cliente),
                },
            )

        self.stdout.write("Vendas importadas")

        # ---------------- ITENS DE VENDA ----------------
        for _, row in df_vendas.iterrows():
            preco_unitario = limpar_decimal(row["Preco_Unitario"])
            desconto = limpar_decimal(row["Desconto_Aplicado"])
            quantidade = int(row["Quantidade"])
            subtotal = preco_unitario * quantidade * (Decimal("1") - (desconto / Decimal("100")))

            ItemVenda.objects.update_or_create(
                venda_id=texto_ou_vazio(row["ID_Venda"]),
                produto_id=texto_ou_vazio(row["ID_Produto"]),
                defaults={
                    "quantidade_vendida": quantidade,
                    "preco_unitario": preco_unitario,
                    "desconto_aplicado": desconto,
                    "subtotal": subtotal,
                },
            )

        self.stdout.write("Itens de venda importados")

        # ---------------- ESTOQUE ----------------
        for _, row in df_produtos.iterrows():
            Estoque.objects.update_or_create(
                produto_id=texto_ou_vazio(row["ID_Produto"]),
                defaults={
                    "quantidade_atual": max(0, int(row["Estoque_Atual"])),
                    "quantidade_minima": int(row["Estoque_Minimo"]),
                    "dt_ultima_saida": tratar_data(row["Data_Ultima_Compra"]),
                },
            )

        self.stdout.write("Estoque importado")

        # ---------------- COMPRAS FORNECEDOR ----------------
        df_compras = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Compras_Fornecedor")

        for id_compra, grupo in df_compras.groupby("ID_Compra"):
            status = texto_ou_vazio(primeiro_valido(grupo, "Status"))
            nota_fiscal = texto_ou_vazio(primeiro_valido(grupo, "Nota_Fiscal"))
            fornecedor_id = texto_ou_vazio(primeiro_valido(grupo, "ID_Fornecedor"))
            valor_total = grupo["Total"].apply(limpar_decimal).sum()

            compra, _ = CompraFornecedor.objects.update_or_create(
                id_compra=texto_ou_vazio(id_compra),
                defaults={
                    "fornecedor_id": fornecedor_id,
                    "funcionario": Funcionario.objects.first(),
                    "data_compra": tratar_data(primeiro_valido(grupo, "Data_Compra")),
                    "status": status,
                    "data_entrega": tratar_data(primeiro_valido(grupo, "Data_Entrega")),
                    "entregue": status.lower() == "entregue",
                    "nota_fiscal": nota_fiscal,
                    "valor_total": valor_total,
                },
            )

            for _, row in grupo.iterrows():
                ItemCompra.objects.update_or_create(
                    compra=compra,
                    produto_id=texto_ou_vazio(row["ID_Produto"]),
                    defaults={
                        "quantidade": int(row["Quantidade"]),
                        "valor_unitario": limpar_decimal(row["Preco_Unitario"]),
                    },
                )

        self.stdout.write("✓ Compras e itens de compra importados")

        # ---------------- DESPESAS ----------------
        df_despesas = pd.read_excel("Mercadinho_Arrumado.xlsx", sheet_name="Despesas")

        for _, row in df_despesas.iterrows():
            Despesa.objects.update_or_create(
                id_despesa=texto_ou_vazio(row["ID_Despesa"]),
                defaults={
                    "funcionario": Funcionario.objects.first(),
                    "compra": None,
                    "data": tratar_data(row["Data"]),
                    "categoria": texto_ou_vazio(row["Categoria"]),
                    "descricao": texto_ou_vazio(row["Descricao"]),
                    "valor": limpar_decimal(row["Valor"]),
                    "recorrente": booleano_da_planilha(row["Recorrente"]),
                },
            )

        self.stdout.write(self.style.SUCCESS("\nImportação concluída com sucesso!"))