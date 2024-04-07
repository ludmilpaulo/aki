from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FornecedorAddProduct, get_all_products, produto_list_view, update_product, delete_product, CategoriaListCreate, shop_get_products, fornecedor_add_product, ProdutoListView, get_fornecedor, ShopCategoryViewSet, ShopViewSet, get_products_by_shop, get_shops_by_category, GetShopsByCategoryView

router = DefaultRouter()
router.register('shop-categories', ShopCategoryViewSet)
router.register('shops', ShopViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('get-products-by-shops/', get_products_by_shop, name='get-products-by-shops'),
    path('get-shops-by-category/', GetShopsByCategoryView.as_view(), name='get_shops_by_category'),
    path('get_fornecedor/', get_fornecedor, name='get_fornecedor'),
  #  path('get_products/', ProdutoListView.as_view()),
    path('add-product/', fornecedor_add_product, name='fornecedor-add-product'),
    path('categorias/', CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('get_products/', shop_get_products, name='fornecedor-get-product'),
   # path('get_products/<int:user_id>/', produto_list_view, name='produto-list'),
    path('delete-product/<int:pk>/', delete_product, name='fornecedor-delete-product'),
    path('update-product/<int:pk>/', update_product, name='update-product'),
    path('get-all-products/', get_all_products, name='get-all-products'),
]
