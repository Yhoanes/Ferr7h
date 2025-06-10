from django.urls import path
from .views import (
    ListarProductos, CrearProducto, EditarProducto, EliminarProducto,
    ListarCategorias, CrearCategoria, EditarCategoria, EliminarCategoria,
    ListarProveedores, CrearProveedor, EditarProveedor, EliminarProveedor
)

urlpatterns = [
    # 📦 Producto
    path('productos/', ListarProductos.as_view(), name='listar_productos'),
    path('productos/crear/', CrearProducto.as_view(), name='crear_producto'),
    path('productos/editar/<int:producto_id>/', EditarProducto.as_view(), name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', EliminarProducto.as_view(), name='eliminar_producto'),

    # 🏷️ Categoría
    path('categorias/', ListarCategorias.as_view(), name='listar_categorias'),
    path('categorias/crear/', CrearCategoria.as_view(), name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', EditarCategoria.as_view(), name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', EliminarCategoria.as_view(), name='eliminar_categoria'),

    # 🏢 Proveedor
    path('proveedores/', ListarProveedores.as_view(), name='listar_proveedores'),
    path('proveedores/crear/', CrearProveedor.as_view(), name='crear_proveedor'),
    path('proveedores/editar/<int:proveedor_id>/', EditarProveedor.as_view(), name='editar_proveedor'),
    path('proveedores/eliminar/<int:proveedor_id>/', EliminarProveedor.as_view(), name='eliminar_proveedor'),
]