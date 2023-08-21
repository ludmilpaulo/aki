from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Fornecedor

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Fornecedor

User = get_user_model()

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
