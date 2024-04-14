from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .permissions import *

from django.db.models import Q


from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView


#from django.contrib.auth.models import User
from rest_framework.parsers import *
from django.contrib.auth import get_user_model
User = get_user_model()


from .models import Image, ProductCategory, ShopCategory, Shop, Product
from .serializers import ProductCategorySerializer, ShopCategorySerializer, ShopSerializer, ProductSerializer

class ShopCategoryViewSet(viewsets.ModelViewSet):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategorySerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def list(self, request, *args, **kwargs):
        category_slug = request.query_params.get('category_slug')
        if category_slug:
            category = ShopCategory.objects.filter(slug=category_slug).first()
            if category:
                queryset = self.queryset.filter(shop_category=category)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
        return super().list(request, *args, **kwargs)



def get_shops_by_category(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
                shops = Shop.objects.filter(shop_category_id=category_id)
                # Assuming you have a serializer for Shop model
                data = [{'id': shop.id, 'name': shop.name, 'phone': shop.phone, 'address': shop.address, 'logo':shop.logo} for shop in shops]
                return JsonResponse(data, safe=False)
            except ValueError:
                return JsonResponse({'error': 'Invalid category ID'}, status=400)
        else:
            return JsonResponse({'error': 'Category ID is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
    



class GetShopsByCategoryView(generics.ListAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
                return Shop.objects.filter(shop_category_id=category_id)
            except ValueError:
                return Shop.objects.none()
        else:
            return Shop.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)




@api_view(['GET'])
def get_products_by_shop(request):
    if request.method == 'GET':
        shop_id = request.GET.get('shop_id')
        if shop_id:
            try:
                products = Product.objects.filter(shop_id=shop_id)
                # Pass request object to serializer context
                serialized_products = ProductSerializer(products, many=True, context={'request': request}).data
                return Response(serialized_products)
            except ValueError:
                return Response({'error': 'Invalid shop ID'}, status=400)
        else:
            return Response({'error': 'Shop ID is required'}, status=400)
    else:
        return Response({'error': 'Only GET method is allowed'}, status=405)
    

def get_fornecedor(request):
    usuario_id = request.GET.get('user_id')

    # Check if the usuario_id parameter is provided
    if usuario_id:
        fornecedores = Shop.objects.filter(user=usuario_id)
    else:
        fornecedores = Shop.objects.all()

    serialized_data = ShopSerializer(
        fornecedores,
        many=True,
        context={"request": request}
    ).data

    return JsonResponse({"fornecedor": serialized_data})


class ProdutoListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)  # Get user_id from the request parameters

        # Get the user object from the user_id
        user = get_object_or_404(User, id=user_id)

        return Product.objects.filter(shop=user.shop).order_by("-id")


from django.core.exceptions import ValidationError

@api_view(["GET"])
def produto_list_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    products = Product.objects.filter(shop=user.shop).order_by("-id")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


    

def shop_get_products(request):
    access_token = request.GET.get('access_token')

    if access_token:
        try:
            # Retrieve the user associated with the access token
            user = Token.objects.get(key=access_token).user

            # Retrieve the shop associated with the user
            shop = user.shop

            # Retrieve products associated with the shop
            products = Product.objects.filter(shop=shop)

            # Serialize the products
            serialized_products = ProductSerializer(products, many=True, context={"request": request}).data

            return JsonResponse({"products": serialized_products})
        except Token.DoesNotExist:
            return JsonResponse({"error": "Invalid access token"}, status=400)
        except AttributeError:
            return JsonResponse({"error": "User or shop not found"}, status=404)
    else:
        return JsonResponse({"error": "Access token is required"}, status=400)



class CategoriaListCreate(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    
    
    
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
        product = Product.objects.get(pk=pk)
        if not hasattr(user, 'shop') or user.shop != product.shop:
            return Response({'error': 'User does not have permission to delete this product'}, status=status.HTTP_403_FORBIDDEN)

        # User is authenticated and has permission, delete the product
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)

        # Check if the user has permission to update the product
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id not provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=user_id)
        if not hasattr(user, 'shop') or user.shop != product.shop:
            return Response({'error': 'User does not have permission to update this product'}, status=status.HTTP_403_FORBIDDEN)

        # Update the product
        product.title = request.data.get('title', product.title)
        product.description = request.data.get('description', product.description)
        product.price = request.data.get('price', product.price)
        product.save()

        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

@api_view(["POST"])
@parser_classes([MultiPartParser])
def fornecedor_add_product(request, format=None):
    data = request.data
    img = [file for key, file in data.items() if key.startswith('images[')]

    print("Received data:", data)  # Print the received data for debugging
    print("Received images:", img)  # Print the received data for debugging

    try:
        # Retrieve the user associated with the access token
        access = Token.objects.get(key=data['access_token']).user

        # Retrieve the shop associated with the user
        shop = access.shop

        # Retrieve or create the category based on the slug
        category_slug = data.get('category')
        if category_slug:
            try:
                category = ProductCategory.objects.get(slug=category_slug)
            except ProductCategory.DoesNotExist:
                category = ProductCategory.objects.create(slug=category_slug, name=category_slug)
        else:
            return Response({'error': 'Category is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a Product instance and associate it with the category, shop, and other fields
        product = Product.objects.create(
            category=category,
            price=data['price'],
            title=data['title'],
            shop=shop,
            description=data['description']
        )

        # Save uploaded images and associate them with the product
        images = []
        for file_field in img:
            # Create an Image instance and save it to the database
            image = Image.objects.create(image=file_field)
            images.append(image)

        # Associate the images with the product
        product.images.set(images)

        return Response({"status": "Product added successfully"}, status=status.HTTP_201_CREATED)

    except Token.DoesNotExist:
        return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser



class FornecedorAddProduct(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        data = request.data

        try:
            # Retrieve the user associated with the access token
            access_token = data.get('access_token')
            user = Token.objects.get(key=access_token).user

            # Retrieve the shop associated with the user
            shop = user.shop

            # Retrieve or create the category based on the slug
            category_slug = data.get('category')
            if category_slug:
                category, created = ProductCategory.objects.get_or_create(slug=category_slug, defaults={'name': category_slug})
            else:
                return Response({'error': 'Category is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a Product instance and associate it with the category, shop, and other fields
            product = Product.objects.create(
                category=category,
                price=data['price'],
                title=data['title'],
                shop=shop,
                description=data['description']
            )

            # Save uploaded images and associate them with the product
            images = []
            for file_field in request.FILES.getlist('images'):
                # Create an Image instance and save it to the database
                image = Image.objects.create(image=file_field)
                images.append(image)

            # Associate the images with the product
            product.images.set(images)

            return Response({"status": "Product added successfully"}, status=status.HTTP_201_CREATED)

        except Token.DoesNotExist:
            return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Assuming this is the backend view function for fetching products
def get_all_products(request):
    search_query = request.GET.get('search', '')

    # Query all products
    products = Product.objects.all()

    # Apply search filter if search query is provided
    if search_query:
        products = products.filter(Q(title__icontains=search_query))
        
    serialized_products = ProductSerializer(products, many=True, context={"request": request}).data


    # Serialize products and return as JSON response
   # serialized_products = [{'id': product.id, 'title': product.title, 'price': product.price, 'image_urls': [str(image) for image in product.images.all()]} for product in products]
    return JsonResponse(serialized_products, safe=False)
