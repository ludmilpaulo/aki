from rest_framework import serializers


#from shop.authentication import User
#User = get_user_model()
from shop.models import Customer, Driver, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use the custom User model
        fields = ['username', 'email', 'is_customer']


class DriverSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_driver=True
        user.save()
        Driver.objects.create(user=user)
        return user




###########################################################################



class CustomerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})

        # Create the user instance
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_customer = True
        user.save()

        # Use the user's primary key to create the associated Customer instance
        customer = Customer.objects.create(user_id=user.pk)

        return user


###############**********************************************
class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Customer
        fields = ("id", "username", "avatar", "phone", "address")


class DriverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Driver
        fields = ("id", "username", "avatar", "phone", "address")


