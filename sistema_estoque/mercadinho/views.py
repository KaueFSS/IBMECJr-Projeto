from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Produto, Estoque
from .serializers import ProdutoSerializer, EstoqueSerializer

# viewset de produtos
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# viewset de estoque
class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.select_related('produto').all()
    serializer_class = EstoqueSerializer

    # extensão da classe que cria um url com todos os produtos cujo estoque está abaixo de seu respectivo mínimo
    @action(detail=False, methods=['get'], url_path='alerta-minimo')
    def alerta(self, request):
        estoques_alerta = Estoque.objects.filter(
            quantidade_atual__lt = F("quantidade_minima")
        )

        serializer = self.get_serializer(estoques_alerta, many=True)

        return Response({
            'total': estoques_alerta.count(),
            'resultados': serializer.data
        })
        