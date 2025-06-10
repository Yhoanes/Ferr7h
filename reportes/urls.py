from django.urls import path
from .views import ReportesVentasView, ApiDatosVentasView, exportar_excel_ventas, exportar_pdf_ventas, ReportesProductosView, exportar_excel_productos, exportar_pdf_productos, ReportesStockSalidaView, ReportesStockEntradaView

urlpatterns = [
    # 🔹 reportes de ventas
    path("ventas/", ReportesVentasView.as_view(), name="reportes_ventas"),
    path("ventas/datos/", ApiDatosVentasView.as_view(), name="api_datos_ventas"),
    path("ventas/exportar_excel/", exportar_excel_ventas, name="exportar_excel_ventas"),
    path("ventas/exportar_pdf/", exportar_pdf_ventas, name="exportar_pdf_ventas"),

    # 🔹 reportes de producto
    path("productos/", ReportesProductosView.as_view(), name="reportes_productos"),
    path("reportes/productos/exportar-excel/", exportar_excel_productos, name="exportar_excel_productos"),
    path("reportes/productos/exportar-pdf/", exportar_pdf_productos, name="exportar_pdf_productos"),
    # 🔹 reportes de stock
    path("stock/salida/", ReportesStockSalidaView.as_view(), name="reportes_stock_salida"),
    path("stock/entrada/", ReportesStockEntradaView.as_view(), name="reportes_stock_entrada"),
]