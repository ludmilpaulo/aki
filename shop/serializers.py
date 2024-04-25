from rest_framework import serializers
from .models import Product, ProductCategory, ServiceCategory, ShopCategory, Shop, Service


class ServiceSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_image_urls(self, obj):
        if obj.images.exists():
            # Get the request object from context
            request = self.context.get('request')
            if request is not None:
                # Build and return absolute URLs for all images associated with the product
                return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return None



class ProductSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image_urls(self, obj):
        if obj.images.exists():
            # Get the request object from context
            request = self.context.get('request')
            if request is not None:
                # Build and return absolute URLs for all images associated with the product
                return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return None


class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'



class ShopSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'phone', 'address', 'logo_url']

    def get_logo_url(self, obj):
        if obj.logo:
            # Assuming you have MEDIA_URL configured in your Django settings
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

