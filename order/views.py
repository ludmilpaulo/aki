from django.http import JsonResponse
from django.shortcuts import get_object_or_404



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView


#from django.contrib.auth.models import User
from rest_framework.parsers import *


from .models import *
from .serializers import OrderSerializer








from django.contrib.auth import get_user_model
User = get_user_model()



AccessToken = Token
##################################################################
#@csrf_exempt
@api_view(['POST'])
def customer_add_order(request):
    data = request.data
    print("recieved data", data)
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)


    if Order.objects.filter(customer=customer).exclude(
            status=Order.DELIVERED):
        return JsonResponse({
            "error": "failed",
            "status": "Seu último pedido deve ser entregue para Pedir Outro."
        })

    # Check Address
    if not data['address']:
        return JsonResponse({
            "status": "failed",
            "error": "Address is required."
        })

    # Get Order Details

    order_details = data["order_details"]


    order_total = 0
    for product in order_details:
        order_total += Product.objects.get(
            id=product["product_id"]).price * product["quantity"]

    if len(order_details) > 0:

            # Step 2 - Create an Order
            order = Order.objects.create(
                customer=customer,
                shop_id=data["shop_id"],
                total=order_total,
                status=Order.COOKING,
                address=data["address"])

            # Step 3 - Create Order details
            for product in order_details:
                OrderDetails.objects.create(
                    order=order,
                    product_id=product["product_id"],
                    quantity=product["quantity"],
                    sub_total=Product.objects.get(id=product["product_id"]).price *
                    product["quantity"])
            #serializer = OrderSerializer(order, many=False)
            return JsonResponse({"status": "success"})
    else:
        return JsonResponse({
            "status": "failed",
            "error": "Failed connect to Stripe."
        })



##############################################################


@api_view(["POST"])
def customer_get_latest_order(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    order = OrderSerializer(
        Order.objects.filter(customer=customer).last()).data

    return JsonResponse({"order": order})

@api_view(["POST"])
def customer_driver_location(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    current_order = Order.objects.filter(customer=customer,
                                         status=Order.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})


# GET params: access_token
@api_view(["POST"])
def customer_get_order_history(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    order_history = OrderSerializer(Order.objects.filter(
        customer=customer, status=Order.DELIVERED).order_by("picked_at"),
                                    many=True,
                                    context={
                                        "request": request
                                    }).data

    return JsonResponse({"order_history": order_history})



@api_view(['POST'])
def shop_order(request, format=None):
     # Print the user to verify if it's retrieved correctly
    data = request.data
    user = get_object_or_404(User, id=data['user_id'])
    print(data)

    try:
        order = Order.objects.get(id=data["id"],
                                shop=user.shop)

        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()

        orders = Order.objects.filter(
        restaurant=user.shop).order_by("-id")

        return Response({'message': 'Order status updated to READY'}, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)  # Get user_id from the request parameters

        # Get the user object from the user_id
        user = get_object_or_404(User, id=user_id)

        return Order.objects.filter(shop=user.shop).order_by("-id")





# GET params: access_token
@api_view(["POST"])
def customer_get_order_history(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    order_history = OrderSerializer(Order.objects.filter(
        customer=customer, status=Order.DELIVERED).order_by("picked_at"),
                                    many=True,
                                    context={
                                        "request": request
                                    }).data

    return JsonResponse({"order_history": order_history})





def shop_order_notification(request, user_id, last_request_time):
    try:
        # Retrieve the user based on the user_id
        user = User.objects.get(id=user_id)
        # Filter orders for the user's shop and created after the last request time
        notification = Order.objects.filter(
            shop=user.shop,
            created_at__gt=last_request_time,
            status=Order.COOKING
        ).count()
        return JsonResponse({"notification": notification})
    except User.DoesNotExist:
        return JsonResponse({"notification": 0}) 
