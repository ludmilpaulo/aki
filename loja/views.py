from rest_framework import viewsets
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.views import ObtainAuthToken


from .models import Fornecedor
from .serializers import FornecedorSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny]) 
def fornecedor_sign_up(request, format=None):
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Nome de usuário e senha são necessários."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "O nome de usuário já existe."}, status=400)

        new_user = User.objects.create_user(username=username, password=password, email=email)
        new_user.e_fornecedor = True
        new_user.save()

        
        request.data._mutable = True  # Allow modifications to the QueryDict
        request.data["usuario"] = new_user.pk

        # Handle uploaded files
        logo = request.FILES.get('logo', None)
        licenca = request.FILES.get('licenca', None)
        if logo:
            request.data['logo'] = logo
        if licenca:
            request.data['licenca'] = licenca

        serializer = FornecedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return Response({
            "token":Token.objects.get(user=user).key,
            'user_id':user.pk,
            "message":"Conta criada com sucesso",
            'username':user.username,
            "status":"201"}, status=201)

        return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def fornecedor_sign_in(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Nome de usuário e senha são necessários."}, status=400)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Add your checks for "fornecedor" here
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "message": "Logado com sucesso",
                "username": user.username,
                "status": "200"
            }, status=200)

        else:
            return Response({"error": "Credenciais inválidas."}, status=401)
    else:
        return Response({"error": "Método inválido."}, status=405)




def get_fornecedor(request):
    usuario_id = request.GET.get('usuario_id')
    
    # Check if the usuario_id parameter is provided
    if usuario_id:
        fornecedores = Fornecedor.objects.filter(usuario=usuario_id)
    else:
        fornecedores = Fornecedor.objects.all()

    serialized_data = FornecedorSerializer(
        fornecedores,
        many=True,
        context={"request": request}
    ).data

    return JsonResponse({"fornecedor": serialized_data})



def get_fornecedor_by_usuario(request, usuario_id):
    fornecedores = Fornecedor.objects.filter(usuario=usuario_id)

    serialized_data = FornecedorSerializer(
        fornecedores,
        many=True,
        context={
            "request": request
        }).data

    return JsonResponse({"fornecedor": serialized_data})


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
