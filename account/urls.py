

from django.urls import path
from . import views

urlpatterns = [
     #####################################################
    path('signup/driver/', views.DriverSignupView.as_view()),
    path('signup/', views.CustomerSignupView.as_view()),
    path('login/',views.CustomAuthToken.as_view(), name='auth-token'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
    path('fornecedor/', views.fornecedor_sign_up),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('customer/profile/update/', views.customer_update_profile),
    path('customer/profile/', views.customer_get_detais),
    ##############################################
] 