from django.contrib import admin
from .models import User, ShopCategory, Shop, Product, ProductCategory, Image

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

