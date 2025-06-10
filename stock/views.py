from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import StockMovimiento
from productos.models import Producto
from .forms import StockMovimientoForm

# 📌 Vista para listar todos los movimientos de stock
class ListarStock(View):
    def get(self, request):
        movimientos = StockMovimiento.objects.all().order_by('-fecha')
        return render(request, 'listar_stock.html', {"movimientos": movimientos})

# 📌 Vista para registrar un nuevo movimiento de stock
class RegistrarMovimientoStock(View):
    def get(self, request):
        form = StockMovimientoForm()
        return render(request, 'registrar_movimiento_stock.html', {"form": form})

    def post(self, request):
        form = StockMovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)

            # 🔹 Obtener el producto asociado
            producto = movimiento.producto

            if movimiento.tipo_movimiento == 'entrada':
                producto.stock += movimiento.cantidad  # 🔹 Incrementar stock
            elif movimiento.tipo_movimiento == 'salida':
                if producto.stock >= movimiento.cantidad:  # 🔹 Validar stock disponible
                    producto.stock -= movimiento.cantidad  # 🔹 Reducir stock
                else:
                    messages.error(request, "No hay suficiente stock disponible.")
                    return render(request, 'registrar_movimiento_stock.html', {"form": form})

            producto.save()
            movimiento.save()
            messages.success(request, "Movimiento de stock registrado exitosamente.")
            return redirect('listar_stock')

        return render(request, 'registrar_movimiento_stock.html', {"form": form})