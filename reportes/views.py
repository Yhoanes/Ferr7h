from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from stock.models import StockMovimiento
from sales.models import Venta
from productos.models import Producto
from django.db.models import Sum
from django.http import HttpResponse
import pandas as pd
from reportlab.pdfgen import canvas

# 🔹 Vista del Reporte de Ventas
@method_decorator(login_required, name="dispatch")
class ReportesVentasView(View):
    def get(self, request):
        ventas = Venta.objects.all().values(
            "fecha", "producto__nombre", "cantidad",
            "producto__precio", "monto_total",
            "cliente__nombre", "pago__tipo_pago", "usuario__username"
        ).order_by("-fecha")

        return render(request, "reportes_ventas.html", {"ventas": ventas})

# 🔹 API para datos de ventas
@method_decorator(login_required, name="dispatch")
class ApiDatosVentasView(View):
    def get(self, request):
        ventas = Venta.objects.values("fecha", "cantidad")
        datos = {
            "fechas": [venta["fecha"].strftime("%Y-%m-%d") for venta in ventas],
            "montos": [venta["cantidad"] for venta in ventas]
        }
        return JsonResponse(datos)
    
# 🔹 Exportar reporte de ventas a Excel
def exportar_excel_ventas(request):
    ventas = Venta.objects.all().values(
        "fecha", "producto__nombre", "cantidad",
        "producto__precio",  # 🔹 Reemplazar 'precio_unitario' por 'producto__precio'
        "monto_total", "cliente__nombre", "pago__tipo_pago", "usuario__username"
    )

    df = pd.DataFrame(ventas)

    # Convertir fechas a formato legible
    df["fecha"] = df["fecha"].apply(lambda x: x.strftime("%Y-%m-%d"))

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.xlsx"'
    df.to_excel(response, index=False)

    return response

# 🔹 Exportar reporte de ventas a PDF
def exportar_pdf_ventas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "📊 Reporte de Ventas")

    ventas = Venta.objects.all().values("fecha", "producto__nombre", "cantidad", "producto__precio",
                                        "monto_total", "cliente__nombre", "pago__tipo_pago", "usuario__username")
    y = 730
    for venta in ventas:
        total_venta = venta["cantidad"] * venta["producto__precio"]
        p.drawString(100, y, f"{venta['fecha']} | {venta['producto__nombre']} | {venta['cantidad']} unidades | ${venta['producto__precio']} c/u | ${venta['monto_total']}")
        y -= 20

    p.showPage()
    p.save()
    return response

# 🔹 Vista del Reporte de Productos
@method_decorator(login_required, name="dispatch")
class ReportesProductosView(View):
    def get(self, request):
        categoria_seleccionada = request.GET.get("categoria", None)
        
        # Filtrar productos por categoría si hay un filtro activo
        productos_mas_vendidos = Producto.objects.annotate(total_vendido=Sum("venta__cantidad")).order_by("-total_vendido")[:10]
        productos_stock = Producto.objects.values("nombre", "categoria__nombre", "stock", "precio")

        if categoria_seleccionada:
            productos_stock = productos_stock.filter(categoria__nombre=categoria_seleccionada)

        categorias = Producto.objects.values_list("categoria__nombre", flat=True).distinct()

        return render(request, "reportes_productos.html", {
            "productos_mas_vendidos": productos_mas_vendidos,
            "productos_stock": productos_stock,
            "categorias": categorias,
        })

# 🔹 Exportar reporte de productos a Excel
def exportar_excel_productos(request):
    productos = Producto.objects.values("nombre", "categoria__nombre", "stock", "precio")

    df = pd.DataFrame(productos)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.xlsx"'
    df.to_excel(response, index=False)

    return response

# 🔹 Exportar reporte de productos a PDF
def exportar_pdf_productos(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "📦 Reporte de Productos")

    productos = Producto.objects.all().values("nombre", "categoria__nombre", "stock", "precio")
    y = 730
    for producto in productos:
        p.drawString(100, y, f"{producto['nombre']} | {producto['categoria__nombre']} | Stock: {producto['stock']} | Precio: ${producto['precio']}")
        y -= 20

    p.showPage()
    p.save()
    return response

# 🔹 Vista del Reporte de Salida de Stock
@method_decorator(login_required, name="dispatch")
class ReportesStockSalidaView(View):
    def get(self, request):
        movimientos_salida = StockMovimiento.objects.filter(tipo_movimiento="salida").values("fecha", "producto__nombre", "cantidad")
        return render(request, "reportes_stock_salida.html", {"movimientos_salida": movimientos_salida})

# 🔹 Vista del Reporte de Entrada de Stock
@method_decorator(login_required, name="dispatch")
class ReportesStockEntradaView(View):
    def get(self, request):
        movimientos_entrada = StockMovimiento.objects.filter(tipo_movimiento="entrada").values("fecha", "producto__nombre", "cantidad")
        return render(request, "reportes_stock_entrada.html", {"movimientos_entrada": movimientos_entrada})
