from django.urls import path
from .views import SalesNewView, SalesHistoryView, ClientsManageView, EditClientView, DeleteClientView, ManageFinancesView, EditDescuentoView, EditMetodoPagoView, DeleteDescuentoView, DeleteMetodoPagoView, ViewSale, RegisterClientView, BuscarClientesView

urlpatterns = [
    path('sales/new/', SalesNewView.as_view(), name='sales_new'),  # Nueva venta
    path('history/', SalesHistoryView.as_view(), name='sales_history'),  # Historial de ventas
    path('clients/', ClientsManageView.as_view(), name='clients_manage'),
    path("clients/register/", RegisterClientView.as_view(), name="register_client"),
    path('clients/edit/<int:client_id>/', EditClientView.as_view(), name='edit_client'),
    path('clients/delete/<int:client_id>/', DeleteClientView.as_view(), name='delete_client'),
    path('finances/', ManageFinancesView.as_view(), name='manage_finances'),
    path('finances/edit-method/<int:metodo_id>/', EditMetodoPagoView.as_view(), name='edit_method'),
    path('finances/edit-discount/<int:descuento_id>/', EditDescuentoView.as_view(), name='edit_discount'),
    path('finances/delete-method/<int:metodo_id>/', DeleteMetodoPagoView.as_view(), name='delete_method'),
    path('finances/delete-discount/<int:descuento_id>/', DeleteDescuentoView.as_view(), name='delete_discount'),
    path("sales/view/<int:venta_id>/", ViewSale.as_view(), name="view_sale"),
    path("sales/buscar_clientes/", BuscarClientesView.as_view(), name="buscar_clientes"),

]