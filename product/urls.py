from django.urls import path
from product.views import HomeView, AboutView, BookingView, MenuView, ContactView, CreateDBView, Product_detail, LoginView, LogoutView, SignupView, VerifyEmail, \
    FavoritesView, VerifyOrder, InformationView, UpdateBookingView, DeleteBooking, PaymentView, HelpFulView, FoodEatenView, ForgotPasswordView, ResetPasswordView, \
    AddFoodToTablesView, FindPartnerView, AcceptInviteView

from product.views_api import ProductProductView

app_name = 'product'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('booking', BookingView.as_view(), name='booking'),
    path('menu', MenuView.as_view(), name='menu'),
    path('service', ContactView.as_view(), name='contact'),
    # path('create-db', CreateDBView.as_view(), name='create-db'),
    path('food/<id>', Product_detail.as_view(), name='food'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify'),
    path('favorites', FavoritesView.as_view(), name='favorites'),
    path('order-verify', VerifyOrder.as_view(), name='order-verify'),
    path('info', InformationView.as_view(), name='info'),
    path('booked', UpdateBookingView.as_view(), name='booked'),
    path('cancel-booking', DeleteBooking.as_view(), name='cancel-booking'),
    path('pay', PaymentView.as_view(),name='pay'),
    path('helpful', HelpFulView.as_view(), name='helpful'),
    path('food-eaten',FoodEatenView.as_view(), name='food-eaten'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('add-food-to-order', AddFoodToTablesView.as_view(), name='add-food-to-order'),
    path('find-partner', FindPartnerView.as_view(), name='find-partner'),
    path('accept-invite', AcceptInviteView.as_view(), name='accept-invite'),

    path('api/v1/product-product', ProductProductView.as_view(), name='product-product')
]