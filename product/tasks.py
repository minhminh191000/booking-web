from .models import Customer, OrderTable, CustomUser
from time import timezone
import pandas as pd
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

def send_mail_verify_order():
    list_customer = Customer.objects.filter(is_send_mail=False)
    for customer in list_customer:
        order = OrderTable.objects.get(customer=customer, is_pending=False)
        time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
        if (order.order_date- time_now).total_seconds() // 60.0 < 20:
            user = CustomUser.objects.get(id=customer.customer_id)
            token = RefreshToken.for_user(customer).access_token
            current_site = 'localhost:8000/home/'#get_current_site(request).domain
            relativeLink = reverse('product:order-verify')
            absurl='http://'+current_site+relativeLink+"?token="+str(token)
            print(absurl)
            data = {
                'email-subject':'Confirm your order',
                'body':'Hi '+ user.full_name+ ', use link bellow to confirm your order:\n '+absurl,
                'to_email': user.email
            }
            Util.send_mail(data)
            customer.is_send_mail = True
            customer.save()
            