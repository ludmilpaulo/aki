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
from rest_framework.generics import ListAPIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.views import ObtainAuthToken


from .models import *
from .serializers import *

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
            fornecedor_instance = user.fornecedor
            login(request, user)
            return Response({
            "token":Token.objects.get(user=user).key,
            'user_id':user.pk,
            "message":"Conta criada com sucesso",
            "fornecedor_id": fornecedor_instance.nome_fornecedor,
            'username':user.username,
            "status":"201"}, status=201)

        return Response(serializer.errors, status=400)



@api_view(["POST"])
@permission_classes((AllowAny,))
def fornecedor_sign_in(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Nome de usuário e senha são necessários."}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the user is a fornecedor
            if not hasattr(user, 'fornecedor'):
                return Response({"error": "O usuário não é um fornecedor."}, status=403)

            # Retrieve the fornecedor instance related to the user
            fornecedor_instance = user.fornecedor

            # You can also extract additional attributes from the fornecedor model
            # and add them to the response if needed
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "message": "Logado com sucesso",
                "username": user.username,
                "fornecedor_id": fornecedor_instance.nome_fornecedor,  # For example, you can return the ID of the Fornecedor instance
                "status": "200"
            }, status=200)

        else:
            return Response({"error": "Credenciais inválidas."}, status=401)
    else:
        return Response({"error": "Método inválido."}, status=405)


class CustomerSignupView(generics.GenericAPIView):
    serializer_class=CustomerSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            'user_id':user.pk,
            "message":"Conta criada com sucesso",
            'username':user.username,
            "status":"201"
        })





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





class ProdutoListView(ListAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)  # Get user_id from the request parameters

        # Get the user object from the user_id
        user = get_object_or_404(User, id=user_id)

        return Produto.objects.filter(fornecedor=user.fornecedor).order_by("-id")

class CategoriaListCreate(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class FornecedorAddProductView(generics.CreateAPIView):
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not hasattr(user, 'fornecedor'):
            return Response({'error': 'User does not have an associated fornecedor'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            #product.fornecedor = Fornecedor.objects.filter(usuario=user_id)
            product.fornecedor = user.fornecedor
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Assuming you've already imported other necessary modules from the code you shared


class FornecedorEditProductView(generics.UpdateAPIView):
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not hasattr(user, 'fornecedor') or user.fornecedor != instance.fornecedor:
            return Response({'error': 'User does not have permission to edit this product'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.permissions import IsAuthenticated

@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    try:
        # Authenticate the user using the user_id from the request
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id not provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=user_id)

        # Check if the user has permission to delete the product
        product = Produto.objects.get(pk=pk)
        if not hasattr(user, 'fornecedor') or user.fornecedor != product.fornecedor:
            return Response({'error': 'User does not have permission to delete this product'}, status=status.HTTP_403_FORBIDDEN)

        # User is authenticated and has permission, delete the product
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Produto.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)









class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
