# Generated by Django 5.2 on 2025-05-27 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_producto_stock'),
        ('sales', '0004_alter_cliente_email_alter_cliente_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='venta',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.producto'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='monto_total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
