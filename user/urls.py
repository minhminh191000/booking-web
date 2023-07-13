from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signin', views.LoginView.as_view(), name='signin'),
    path('signup', views.SignupView.as_view(), name='signup'),
]