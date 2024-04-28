from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceListCreate, delete_service, fornecedor_add_service, get_all_products, shop_get_service, update_product, delete_product, CategoriaListCreate, shop_get_products, fornecedor_add_product, ProdutoListView, get_fornecedor, ShopCategoryViewSet, ShopViewSet, get_products_by_shop, get_shops_by_category, GetShopsByCategoryView, ServiceListAPIView, ServiceDetailAPIView, ServiceRequestCreateAPIView

router = DefaultRouter()
router.register('shop-categories', ShopCategoryViewSet)
router.register('shops', ShopViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('get-products-by-shops/', get_products_by_shop, name='get-products-by-shops'),
    path('get-shops-by-category/', GetShopsByCategoryView.as_view(), name='get_shops_by_category'),
    path('get_fornecedor/', get_fornecedor, name='get_fornecedor'),
    path('add-product/', fornecedor_add_product, name='fornecedor-add-product'),
    path('categorias/', CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('get_products/', shop_get_products, name='fornecedor-get-product'),
    path('delete-product/<int:pk>/', delete_product, name='fornecedor-delete-product'),
    path('update-product/<int:pk>/', update_product, name='update-product'),
    path('get-all-products/', get_all_products, name='get-all-products'),

    path('add-service/', fornecedor_add_service, name='fornecedor-add-service'),
    path('get_services/', shop_get_service, name='get-all-services'),
    path('delete-service/<int:pk>/', delete_service, name='fornecedor-delete-service'),
    path('services_categorias/', ServiceListCreate.as_view(), name='categoria-list-create'),
    
    path('services/', ServiceListAPIView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('service-requests/', ServiceRequestCreateAPIView.as_view(), name='service-request-create'),
 
]
