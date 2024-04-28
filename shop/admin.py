from django.contrib import admin
from .models import ServiceImage, User, ShopCategory, Shop, Product, ProductCategory, Image, Customer, Driver, Service, ServiceCategory


@admin.register(ServiceImage)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceCategory)
class ServiceAdmin(admin.ModelAdmin):
    pass
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

