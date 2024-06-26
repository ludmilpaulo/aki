# Generated by Django 5.0.4 on 2024-04-26 18:55

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0005_servicecategory_serviceimage_service'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, verbose_name='Endereco')),
                ('total', models.IntegerField()),
                ('status', models.IntegerField(choices=[(1, 'Cozinhando'), (2, 'Pedido Pronto'), (3, 'A caminho'), (4, 'Entregue')], verbose_name='stado')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='criado em')),
                ('picked_at', models.DateTimeField(blank=True, null=True, verbose_name='pegar em')),
                ('chat', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_chat', to='order.chat')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer', verbose_name='cliente')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.driver', verbose_name='motorista')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop', verbose_name='restaurante')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.AddField(
            model_name='chat',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='order.order'),
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantidade')),
                ('sub_total', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='order.order', verbose_name='Pedido')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Refeição')),
            ],
            options={
                'verbose_name': 'Detalhe do pedido',
                'verbose_name_plural': 'Detalhes dos pedidos',
            },
        ),
    ]
