from django import forms
from .models import StockMovimiento

class StockMovimientoForm(forms.ModelForm):
    class Meta:
        model = StockMovimiento
        fields = ['producto', 'tipo_movimiento', 'motivo', 'cantidad', 'comentario']
        
        widgets = {
            'tipo_movimiento': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }