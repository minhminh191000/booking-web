from django.urls import path
from user.views import HomeView, LoginView, SignupView
from user.views_api import LoginAPIView

app_name = 'user'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signin', LoginView.as_view(), name='signin'),
    path('signup', SignupView.as_view(), name='signup'),
    path('api/v1/login', LoginAPIView.as_view(), name='login api'),
    
]