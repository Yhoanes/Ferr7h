from django.db import models

# Modelo de Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo de Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    contacto = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    proveedores = models.ManyToManyField('Proveedor')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # 🔹 Nuevo campo

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"
