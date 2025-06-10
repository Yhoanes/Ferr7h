from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Producto, Categoria, Proveedor
from .forms import ProductoForm, CategoriaForm, ProveedorForm

# 📦 CRUD de Producto
class ListarProductos(View):
    def get(self, request):
        productos = Producto.objects.all()
        return render(request, 'listar_productos.html', {"productos": productos})

class CrearProducto(View):
    def get(self, request):
        form = ProductoForm()
        return render(request, 'crear_producto.html', {"form": form})

    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["precio"] > 0:  # 🔹 Validación: Precio positivo
                form.save()
                messages.success(request, "Producto creado exitosamente.")
                return redirect('listar_productos')
            else:
                form.add_error("precio", "El precio debe ser mayor a 0.")
        return render(request, 'crear_producto.html', {"form": form})

class EditarProducto(View):
    def get(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        form = ProductoForm(instance=producto)
        return render(request, 'editar_producto.html', {"form": form, "producto": producto})

    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            if form.cleaned_data["precio"] > 0:  # 🔹 Validación antes de guardar
                form.save()
                messages.success(request, "Producto actualizado correctamente.")
                return redirect('listar_productos')
            else:
                form.add_error("precio", "El precio debe ser mayor a 0.")
        return render(request, 'editar_producto.html', {"form": form, "producto": producto})

class EliminarProducto(View):
    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('listar_productos')

# 🏷️ CRUD de Categoría
class ListarCategorias(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(request, 'listar_categorias.html', {"categorias": categorias})

class CrearCategoria(View):
    def get(self, request):
        form = CategoriaForm()
        return render(request, 'crear_categoria.html', {"form": form})

    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect('listar_categorias')
        return render(request, 'crear_categoria.html', {"form": form})

class EditarCategoria(View):
    def get(self, request, categoria_id):
        categoria = get_object_or_404(Categoria, id=categoria_id)
        form = CategoriaForm(instance=categoria)
        return render(request, 'editar_categoria.html', {"form": form, "categoria": categoria})

    def post(self, request, categoria_id):
        categoria = get_object_or_404(Categoria, id=categoria_id)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('listar_categorias')
        return render(request, 'editar_categoria.html', {"form": form, "categoria": categoria})

class EliminarCategoria(View):
    def post(self, request, categoria_id):
        categoria = get_object_or_404(Categoria, id=categoria_id)
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('listar_categorias')

# 🏢 CRUD de Proveedor
class ListarProveedores(View):
    def get(self, request):
        proveedores = Proveedor.objects.all()
        return render(request, 'listar_proveedores.html', {"proveedores": proveedores})

class CrearProveedor(View):
    def get(self, request):
        form = ProveedorForm()
        return render(request, 'crear_proveedor.html', {"form": form})

    def post(self, request):
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado exitosamente.")
            return redirect('listar_proveedores')
        return render(request, 'crear_proveedor.html', {"form": form})

class EditarProveedor(View):
    def get(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        form = ProveedorForm(instance=proveedor)
        return render(request, 'editar_proveedor.html', {"form": form, "proveedor": proveedor})

    def post(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect('listar_proveedores')
        return render(request, 'editar_proveedor.html', {"form": form, "proveedor": proveedor})

class EliminarProveedor(View):
    def post(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('listar_proveedores')