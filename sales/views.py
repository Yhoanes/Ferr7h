from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from decimal import Decimal, InvalidOperation
from .models import Cliente, Venta, Pago, MetodoPago, Descuento
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from productos.models import Producto
from .forms import VentaForm


@method_decorator(login_required, name='dispatch')
class SalesNewView(View):
    def get(self, request):
        form = VentaForm()
        clientes = Cliente.objects.all()
        metodos_pago = MetodoPago.objects.all()
        descuentos = Descuento.objects.all()
        productos = Producto.objects.all()

        return render(request, 'new_sale.html', {
            "form": form,
            "clientes": clientes,
            "metodos_pago": metodos_pago,
            "descuentos": descuentos,
            "productos": productos
        })

    def post(self, request):
        form = VentaForm(request.POST)

        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto
            usuario = request.user  # 🔹 Capturamos el usuario autenticado
            
            # 🔹 Validamos stock antes de procesar la venta
            if producto.stock < venta.cantidad:
                messages.error(request, "No hay suficiente stock disponible.")
                return redirect("sales_new")

            # 🔹 Asociamos el usuario a la venta
            venta.usuario = usuario

            # 🔹 Reducimos el stock y guardamos los datos
            producto.stock -= venta.cantidad
            producto.save()
            venta.save()

            messages.success(request, "Venta registrada correctamente y stock actualizado.")
            return redirect("sales_history")
        
        messages.error(request, "Hubo un error en el formulario.")
        return render(request, 'new_sale.html', {
            "form": form,
            "clientes": Cliente.objects.all(),
            "metodos_pago": MetodoPago.objects.all(),
            "descuentos": Descuento.objects.all(),
            "productos": Producto.objects.all()
        })


@method_decorator(login_required, name='dispatch')
class SalesHistoryView(View):
    def get(self, request):
        ventas = Venta.objects.all().order_by("-fecha")
        metodos_pago = MetodoPago.objects.all()
        mensaje = "No hay ventas registradas aún." if not ventas.exists() else None
        return render(request, 'sales_history.html', {
            "ventas": ventas,
            "metodos_pago": metodos_pago,
            "mensaje": mensaje
        })

@method_decorator(login_required, name='dispatch')
class ViewSale(View):
    def get(self, request, venta_id):
        venta = get_object_or_404(Venta, id=venta_id)
        return render(request, "view_sale.html", {"venta": venta})

@method_decorator(login_required, name='dispatch')
class BuscarClientesView(View):
    def get(self, request):
        query = request.GET.get("query", "").strip().lower()

        if not query:
            return JsonResponse([], safe=False)

        clientes = Cliente.objects.filter(nombre__icontains=query).values("id", "nombre")
        return JsonResponse(list(clientes), safe=False)

@method_decorator(login_required, name='dispatch')
class ClientsManageView(View):
    def get(self, request):
        clientes = Cliente.objects.all()
        return render(request, "clients_manage.html", {"clientes": clientes})

@method_decorator(login_required, name='dispatch')
class RegisterClientView(View):
    def post(self, request):
        nombre = request.POST.get("nombre")
        email = request.POST.get("email").strip() if request.POST.get("email") else ""
        telefono = request.POST.get("telefono")

        if not nombre:
            return JsonResponse({"success": False, "error": "El nombre es obligatorio."}, status=400)

        cliente = Cliente.objects.create(nombre=nombre, email=email, telefono=telefono)

        next_url = request.POST.get("next")

        # 🔹 Siempre devolver JSON en lugar de redirigir
        if next_url == "sales_new":
            return JsonResponse({"success": True, "cliente_id": cliente.id, "nombre": cliente.nombre})
        
        return JsonResponse({"success": True, "cliente_id": cliente.id, "nombre": cliente.nombre})  # 🔹 Quitamos la redirección

@method_decorator(login_required, name='dispatch')
class EditClientView(View):
    def get(self, request, client_id):
        cliente = get_object_or_404(Cliente, id=client_id)
        return render(request, "edit_client.html", {"cliente": cliente})

    def post(self, request, client_id):
        cliente = get_object_or_404(Cliente, id=client_id)
        cliente.nombre = request.POST.get("nombre")
        cliente.email = request.POST.get("email")
        cliente.telefono = request.POST.get("telefono")
        cliente.save()
        return redirect("clients_manage")

@method_decorator(login_required, name='dispatch')
class DeleteClientView(View):
    def post(self, request, client_id):
        cliente = get_object_or_404(Cliente, id=client_id)
        cliente.delete()
        return redirect("clients_manage")

@method_decorator(login_required, name='dispatch')
class ManageFinancesView(View):
    def get(self, request):
        metodos_pago = MetodoPago.objects.all()
        descuentos = Descuento.objects.all()
        return render(request, "manage_finances.html", {"metodos_pago": metodos_pago, "descuentos": descuentos})

    def post(self, request):
        if "nombre_metodo" in request.POST:  
            MetodoPago.objects.create(nombre=request.POST["nombre_metodo"])

        if "nombre_descuento" in request.POST:  
            Descuento.objects.create(nombre=request.POST["nombre_descuento"], porcentaje=request.POST["porcentaje"])

        return redirect("manage_finances")

@method_decorator(login_required, name='dispatch')
class EditMetodoPagoView(View):
    def get(self, request, metodo_id):
        metodo_pago = get_object_or_404(MetodoPago, id=metodo_id)
        return render(request, "edit_method.html", {"metodo_pago": metodo_pago})

    def post(self, request, metodo_id):
        metodo_pago = get_object_or_404(MetodoPago, id=metodo_id)
        metodo_pago.nombre = request.POST.get("nombre_metodo")
        metodo_pago.save()
        return redirect("manage_finances")

@method_decorator(login_required, name='dispatch')
class EditDescuentoView(View):
    def post(self, request, descuento_id):
        descuento = get_object_or_404(Descuento, id=descuento_id)
        porcentaje = int(request.POST.get("porcentaje"))

        if porcentaje < 1:  
            return redirect("manage_finances")

        descuento.nombre = request.POST.get("nombre_descuento")
        descuento.porcentaje = porcentaje
        descuento.save()
        return redirect("manage_finances")

@method_decorator(login_required, name='dispatch')
class DeleteMetodoPagoView(View):
    def post(self, request, metodo_id):
        metodo_pago = get_object_or_404(MetodoPago, id=metodo_id)
        metodo_pago.delete()
        return redirect("manage_finances")

@method_decorator(login_required, name='dispatch')
class DeleteDescuentoView(View):
    def post(self, request, descuento_id):
        descuento = get_object_or_404(Descuento, id=descuento_id)
        descuento.delete()
        return redirect("manage_finances")