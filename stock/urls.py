from django.urls import path
from .views import ListarStock, RegistrarMovimientoStock

urlpatterns = [
    path('listar/', ListarStock.as_view(), name='listar_stock'),
    path('registrar/', RegistrarMovimientoStock.as_view(), name='registrar_movimiento_stock'),
]