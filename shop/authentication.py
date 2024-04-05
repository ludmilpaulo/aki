from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class CustomAuthentication(BaseAuthentication):
   def authenticate(self, request):
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')

        print(f'User ID: {user_id}')
        print(f'Access Token: {access_token}')

        if not user_id or not access_token:
            return None

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        try:
            token = Token.objects.get(key=access_token, user=user)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid access token')

        return (user, None)

