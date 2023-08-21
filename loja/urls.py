# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
  
    # urls.py (continued...)
    path('api/fornecedor-sign-up/', fornecedor_sign_up, name='fornecedor_sign_up'),
    path('api/fornecedor_sign_in/', fornecedor_sign_in, name='fornecedor_sign_in'),
    path('api/get_fornecedor/', get_fornecedor, name='get_fornecedor'),

    # ... your other urlpatterns
]
