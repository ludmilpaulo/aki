from django.contrib import admin
from .models import Order, OrderDetails

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    pass