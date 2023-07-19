# from ist.serializers.serializers import ISTStatusViewCreateSerializer

from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework import generics, status, views, permissions
from rest_framework_simplejwt.tokens import AccessToken
import jwt

from django.contrib.auth import authenticate



# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {
        'refresh': str(refresh),
        'access': str(access),
    }


class LoginServices:

    @classmethod
    def login_api(cls, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_admin:
                token = get_tokens_for_user(user)
                return token    
        return False
    