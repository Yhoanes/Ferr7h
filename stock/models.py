from django.db import models
from productos.models import Producto
from django.utils.timezone import now

class StockMovimiento(models.Model):
    MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    MOTIVO_CHOICES = [
        ('compra_proveedor', 'Compra a proveedor'),
        ('devolucion', 'Devolución de cliente'),
        ('nuevo_ingreso', 'Nuevo ingreso'),
        ('venta', 'Venta'),
        ('producto_dañado', 'Producto dañado'),
        ('robo', 'Robo'),
        ('retiro', 'Retiro de inventario'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=10, choices=MOVIMIENTO_CHOICES)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=now)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} ({self.cantidad}) - {self.motivo}"