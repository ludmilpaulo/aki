from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Fornecedor

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Fornecedor, Produto, Categoria

User = get_user_model()

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    # Explicitly declare the categoria as a CharField
    categoria = serializers.CharField()

    class Meta:
        model = Produto
        fields = '__all__'

    def create(self, validated_data):
        # Get the categoria slug from the validated_data
        categoria_slug = validated_data.pop('categoria')

        # Use get_or_create to either fetch the Categoria with the given slug or create a new one
        categoria_instance, created = Categoria.objects.get_or_create(slug=categoria_slug)

        # Replace the slug with the actual Categoria instance
        validated_data['categoria'] = categoria_instance

        # Create and return the Produto instance
        return Produto.objects.create(**validated_data)

class FornecedorSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    logo = serializers.SerializerMethodField()

    def get_logo(self, fornecedor):
        request = self.context.get('request')
        logo_url = fornecedor.logo.url if fornecedor.logo else None
        return request.build_absolute_uri(logo_url) if logo_url else None

    class Meta:
        model = Fornecedor
        fields = '__all__'
