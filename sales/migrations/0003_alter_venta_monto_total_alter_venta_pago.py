# Generated by Django 5.2 on 2025-05-20 19:37

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_descuento_porcentaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='monto_total',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='venta',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.pago'),
        ),
    ]
