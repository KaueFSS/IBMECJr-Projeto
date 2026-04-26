from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Produto, Estoque
from .serializers import ProdutoSerializer, EstoqueSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.select_related('produto').all()
    serializer_class = EstoqueSerializer

    @action(detail=False, methods=['get'], url_path='alerta-minimo')
    def alerta(self, request):
        estoques_alerta = Estoque.objects.filter(
            quantidade_atual__lt = F("estoque_minimo")
        )

        serializer = self.get_serializer(estoques_alerta, many=True)

        return Response({
            'total': itens_em_alerta.count(),
            'resultados': serializer.data
        })
        