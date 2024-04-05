from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.conf import settings

from shop.models import Customer, Driver, Product, Shop

class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cozinhando"),
        (READY, "Pedido Pronto"),
        (ONTHEWAY, "A caminho"),
        (DELIVERED, "Entregue"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='cliente')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='restaurante')
    driver = models.ForeignKey(Driver, blank=True, null=True, on_delete=models.CASCADE, verbose_name='motorista')  # can be blank
    address = models.CharField(max_length=500, verbose_name='Endereco')
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name='stado')
    chat = models.OneToOneField('order.Chat', on_delete=models.CASCADE, null=True, blank=True, related_name='order_chat')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='criado em')
    picked_at = models.DateTimeField(blank=True, null=True, verbose_name='pegar em')


    class Meta:
        verbose_name ='Pedido'
        verbose_name_plural ='Pedidos'

    def __str__(self):
        return str(self.shop)




class Chat(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='chat_messages')
   # sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE, verbose_name='Pedido')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Refeição')
    quantity = models.IntegerField(verbose_name='Quantidade')
    sub_total = models.IntegerField()

    class Meta:
        verbose_name ='Detalhe do pedido'
        verbose_name_plural ='Detalhes dos pedidos'



    def __str__(self):
        return str(self.product)



