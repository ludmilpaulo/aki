from django.urls import path
from . import views

urlpatterns = [
    path('customer/add_order/', views.customer_add_order, name='customer_add_order'),
    path('customer/get_latest_order/', views.customer_get_latest_order, name='customer_get_latest_order'),
    path('customer/driver_location/', views.customer_driver_location, name='customer_driver_location'),
    path('customer/get_order_history/', views.customer_get_order_history, name='customer_get_order_history'),
    path('shop/status/', views.shop_order, name='shoo_order_api'),
    path('shop/orders/',views.OrderListView.as_view()),

]
