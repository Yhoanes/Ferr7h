from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator  # IMPORTANTE
from productos.models import Producto


# Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, unique=False)  # Ya no es único cuando está vacío
    telefono = models.CharField(max_length=20, blank=True, default="")

# Descuento
class Descuento(models.Model):
    nombre = models.CharField(max_length=100)
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(100)]  # Limita entre 1 y 100
    )

# Método de Pago
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Pago asociado a una Venta
class Pago(models.Model):
    tipo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_pago} - {self.monto} Bs"

# Venta
class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, null=True, blank=True)
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.producto:
            self.monto_total = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)
