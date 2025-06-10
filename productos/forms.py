from django import forms
from .models import Producto, Categoria, Proveedor

# 📦 Formulario para Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'proveedores', 'precio'] 
        widgets = {
            'proveedores': forms.CheckboxSelectMultiple()
        }

# 🏷️ Formulario para Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

# 🏢 Formulario para Proveedor
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'email']