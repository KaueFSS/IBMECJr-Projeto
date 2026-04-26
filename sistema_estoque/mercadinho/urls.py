from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, EstoqueViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'estoques', EstoqueViewSet, basename='estoque')

# inclui automaticamente todas as rotas para cada operação crud de cada model
urlpatterns = [
    path('', include(router.urls)),
]