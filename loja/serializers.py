from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Fornecedor

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import *

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

class CustomerSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }


    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_customer=True
        user.save()
        Customer.objects.create(user=user)
        return user
###############**********************************************

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'