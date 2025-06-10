from django import forms
from .models import Venta, Producto, Cliente, MetodoPago, Descuento


class VentaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'})
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    metodo_pago = forms.ModelChoiceField(
        queryset=MetodoPago.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    descuento = forms.ModelChoiceField(
        queryset=Descuento.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'cliente', 'metodo_pago', 'descuento', 'monto_total']
