from django.urls import path
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),
    path('booking', views.BookingView.as_view(), name='booking'),
    path('menu', views.MenuView.as_view(), name='menu'),
    path('service', views.ContactView.as_view(), name='contact'),
    # path('create-db', views.CreateDBView.as_view(), name='create-db'),
    path('food/<id>', views.Product_detail.as_view(), name='food'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
    path('favorites', views.FavoritesView.as_view(), name='favorites'),
    path('order-verify', views.VerifyOrder.as_view(), name='order-verify'),
    path('info', views.InformationView.as_view(), name='info'),
    path('booked', views.UpdateBookingView.as_view(), name='booked'),
    path('cancel-booking', views.DeleteBooking.as_view(), name='cancel-booking'),
    path('pay', views.PaymentView.as_view(),name='pay'),
    path('helpful', views.HelpFulView.as_view(), name='helpful'),
    path('food-eaten',views.FoodEatenView.as_view(), name='food-eaten'),
    path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    path('add-food-to-order', views.AddFoodToTablesView.as_view(), name='add-food-to-order'),
    path('find-partner', views.FindPartnerView.as_view(), name='find-partner'),
    path('accept-invite', views.AcceptInviteView.as_view(), name='accept-invite')
]