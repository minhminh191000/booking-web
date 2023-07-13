from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse,JsonResponse
from .models import Category, Product, Image_Product, Customer, CustomUser, Favorite, TypeTable, OrderTable, Order, Payment, ProductSold,DiscountBill, TypeCustomer, Comment_product, Comment, Invite
import asyncio
from django.contrib.auth.hashers import check_password
from django.db.models import F, Q
from django.template.loader import render_to_string
import re
import json
import pandas as pd
from .forms import SignupForm, UpdateForm, UpdateFormFull
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.exceptions import ValidationError
import time
from django.utils import timezone
from datetime import datetime, timedelta
from .tasks import send_mail_verify_order
# Create your views here.

send_mail_verify_order()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def getName(request):
    name = ''
    customer = None
    list_favorites=[]
    notification = False
    if request.user.is_authenticated:
        try:
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            invites = Invite.objects.filter(Q(customer=customer)&Q(time_invite__gt = time_now)&Q(is_confirm = False))
            if invites:
                notification = False
            customer = Customer.objects.get(customer_id = request.user.id)
            # print(request.user.customer.is_order)
            name = request.user.full_name.split()[-1]
            list_favorites = Favorite.objects.filter(customer_id = customer.id).values_list('product_id', flat=True)
        except:
            pass

    return name, customer, list_favorites, notification


class HomeView(View):
    def get(self, request, *args, **kwargs):
        name, customer,list_favorites, notification = getName(request)
        most_food = Product.objects.filter(Q(rate__gt = 4) & Q(status=True))[:8]
        try:
            if customer:
                time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
                list_pay = Payment.objects.filter(Q(status=False)&Q(order_detail__customer =customer) &Q(order_detail__status = True))
                for pay in list_pay:
                    if pay.order_detail.intend_time < time_now:
                        pay.status=True
                        order_food = pay.order_detail.order_set.all()
                        if order_food:
                            try:
                                user_comment = Comment_product.objects.get(customer = customer)
                            except:
                                user_comment = Comment_product(customer=customer).save()
                            for food in order_food:
                                try:
                                    sold = ProductSold.objects.get(product = food.product)
                                    sold.sold += food.quantity
                                except:
                                    sold = ProductSold(product = food.product, sold = food.quantity)
                                user_comment.is_comment.add(food.product)
                                user_comment.food_eaten.add(food.product)
                                user_comment.save()
                                sold.save()
                        pay.save()
                if customer.is_order:
                    time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ordered = OrderTable.objects.filter( Q(customer=customer) & Q(intend_time__gt=time_now) & Q(status=True))
                    if not ordered:
                        customer.is_order = False
                        customer.save()
        except:
            pass
        return render(request,'product/index.html',
                      {'name':name,
                       'customer': request.user,
                       'list_favorites': list_favorites,
                       'most_food': most_food,
                       'notification':notification})

class AboutView(View):
    def get(self, request, *args, **kwargs):
        name,_, list_favorites,notification = getName(request)
        return render(request, 'product/about.html',
                      {'name':name,
                       'list_favorites':list_favorites,
                       'notification':notification})

class MenuView(View):
    def get(self, request, *args, **kwargs):
        name,customer, list_favorites,notification = getName(request)
        ordered = None
        is_order = ''
        if customer:
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            ordered = OrderTable.objects.filter( Q(customer=customer) & Q(order_date__gt=time_now) & Q(status=True))
            is_order = False
            if ordered:
                is_order = True
        if not is_ajax(request):
            list_category = Category.objects.filter(status=True)
            list_product = Product.objects.filter(status=True).order_by('name')[:30]
            return render(request, 'product/menu.html',
                          {'list_category': list_category,
                           'list_product': list_product,
                           'list_favorites': list_favorites,
                           'customer': customer,
                           'ordered': ordered,
                           'is_order':is_order,
                           'notification':notification,
                            'name': name})
        else:
            filter_food = {
                'status': True,
            }
            category = request.GET.get('category')
            if category:
                filter_food['category'] = category
            name = request.GET.get('name')
            rate_4 = request.GET.get('rate')
            if name:
                if rate_4:
                    list_product = Product.objects.filter(name__istartswith= name,rate__gte = 4,**filter_food).order_by("id")
                else:
                    list_product = Product.objects.filter(name__istartswith= name,**filter_food).order_by("id")
            else:
                if rate_4:
                    list_product = Product.objects.filter(rate__gte = 4,**filter_food).order_by("id")
                else:
                    list_product = Product.objects.filter(**filter_food).order_by("id")
            by_rate = request.GET.get('by_rate')
            if by_rate:
                list_product = list_product.order_by("-rate" if by_rate=="desc" else "rate")

            by_price = request.GET.get('by_price')
            if by_price:
                list_product = list_product.order_by("-price" if by_price=="desc" else "price")

            page_number = request.GET.get('page')
            paginator = Paginator(list_product,30)
            try:
                products = paginator.get_page(page_number)
            except PageNotAnInteger:
                page_number = 1
                products = paginator.get_page(page_number)
            except EmptyPage:
                page_number = paginator.num_pages
                products = paginator.get_page(page_number)
            content = ''
            for product in products:
                content += render_to_string('product/food-items.html',
                                            {'product': product, 'list_favorites': list_favorites,'is_order':is_order,},
                                            request=request)
            return JsonResponse({
                "content": content,
                "end_pagination": True if int(page_number) >= paginator.num_pages else False,
            })

class Product_detail(View):
    def get(self, request, id, *args, **kwargs):
        name,customer,list_favorites,notification = getName(request)
        pro = Product.objects.get(id=id)
        recommended = Product.objects.filter(category_id = pro.category_id).exclude(id=id)[:20]
        img_detail = pro.product.all()
        can_comment = False
        list_comments = None
        ordered = None
        is_order = ''
        if customer:
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            ordered = OrderTable.objects.filter( Q(customer=customer) & Q(order_date__gt=time_now) & Q(status=True))
            is_order = False
            if ordered:
                is_order = True
        try:
            list_comments = pro.comment_set.all()
            # print(list_comments)
        except:
            pass
        try:
            comment = Comment_product.objects.get(customer=customer).is_comment.all()
            if pro in comment:
                can_comment = True
        except:
            pass
        return render(request,"product/product_detail.html",
                      {'name': name,
                       'product': pro,
                       'ordered': ordered,
                        'is_order':is_order,
                       'recommended': recommended,
                       'comments': list_comments,
                       'img_detail': img_detail,
                       'len_img': len(img_detail),
                       'list_favorites': list_favorites,
                       'notification':notification,
                       'can_comment': can_comment})
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            food_id = request.POST.get('food_id')
            rating = request.POST.get('rating')
            cmt = request.POST.get('comment')
            try:
                product = Product.objects.get(id=food_id)
                Comment(customer = request.user.customer,product=product,rate=rating, comment=cmt).save()
                cmt_pro = Comment_product.objects.get(customer = request.user.customer)
                avg_rate = list(product.comment_set.all().values_list('rate', flat=True))
                # print(sum(avg_rate)/len(avg_rate))
                product.rate = sum(avg_rate)/len(avg_rate)
                product.save()
                cmt_pro.is_comment.remove(product)
                cmt_pro.save()
                return JsonResponse({"msg":'Success'})
            except:
                return JsonResponse({"msg":'Comment failed'}, status=400)
        return JsonResponse({'msg': 'Method not allowed!'}, status=401)

class HelpFulView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            id = request.POST.get('id')
            cate = request.POST.get('category')
            if id and cate:
                try:
                    cmt = Comment.objects.get(id=id)
                    list_customers = getattr(cmt, 'user_'+cate)
                    if request.user.customer not in list_customers.all():
                        old_value = getattr(cmt, cate)
                        setattr(cmt, cate, old_value + 1)
                        list_customers.add(request.user.customer)
                    else:
                        old_value = getattr(cmt, cate)
                        setattr(cmt, cate, old_value - 1)
                        list_customers.remove(request.user.customer)
                    cmt.save()
                    return JsonResponse({'msg':'success',cate:getattr(cmt, cate)})
                except:
                    pass
            return JsonResponse({'msg':'Fail'}, status=400)
        return JsonResponse({'msg':'Method not allowed!'}, status=401)

class ContactView(View):
    def get(self, request, *args, **kwargs):
        name,_, list_favorites,notification = getName(request)
        return render(request, 'product/contact.html',
                      {'name': name,
                       'list_favorites': list_favorites,
                       'notification':notification})

class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'product/login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active and not user.is_admin:
            login(request, user)
            return JsonResponse({"url":redirect('product:home').url}, status=200)
        else:
            return JsonResponse({"message":"Email or password not correct"}, status=400)

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('product:home')

class SignupView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'product/signup.html')

    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email = request.POST.get('email'), phone_number = request.POST.get('phone_number'))
            if user.create_not_signup:
                password = request.POST.get('password')
                password2 = request.POST.get('password2')
                if len(password)<8 or password!=password2:
                    return JsonResponse({"password2":[{"message":"Two password must be at least 8 characters and match together!"}]}, status=400)
                user.create_not_signup = False
                user.full_name = request.POST.get('full_name')
                user.address = request.POST.get('address')
                user.set_password(request.POST.get('password'))
                type_customer = TypeCustomer.objects.get(id=1)
                user.rank = type_customer
                user.save()
            else:
                return JsonResponse({"password2":[{"message":"Email or phone number is used"}]}, status=400)
        except:
            form = SignupForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    type_customer = TypeCustomer.objects.get(id=1)
                    user.rank = type_customer
                    user.save()
                    Customer(customer=user).save()
                except:
                    return JsonResponse({"password2":[{"message":"Email or phone number not correct format"}]}, status=400)
            else:
                err = form.errors.get_json_data()
                return JsonResponse(err, status=400)
        try:
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('product:email-verify')
            absurl='http://'+current_site+relativeLink+"?token="+str(token)
            print(absurl)
            #send mail
            data = {
                'email-subject':'Verify your email',
                'body':'Hi '+ user.full_name+ ', use link bellow to verify your email:\n '+absurl,
                'to_email': user.email
            }
            Util.send_mail(data)
            content = render_to_string('product/verify-email.html',
                                        {'email':user.email},
                                            request=request)
            return JsonResponse({"content":content})
        except:
             return JsonResponse({"password2":[{"message":"OPP! Something is wrong."}]}, status=400)

class VerifyEmail(TemplateView):
    def get(self, request):
        try:
            token = request.GET.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            customer = CustomUser.objects.get(id=payload['user_id'])
            if not customer.is_active:
                customer.is_active = True
                customer.save()
            return render(request, 'product/confirm.html')
        except jwt.ExpiredSignatureError:
            return render(request,'product/404.html')

class VerifyOrder(TemplateView):
    def get(self, request):
        try:
            token = request.GET.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            customer = Customer.objects.get(id=payload['user_id'])
            if customer.is_order:
                order_table = OrderTable.objects.get(customer=customer)
                order_table.is_pending =True
                order_table.save()
            return render(request, 'product/confirm.html')

        except jwt.ExpiredSignatureError:
            return render(request,'product/404.html')

class FavoritesView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            name, customer, list_favorites,notification = getName(request)
            list_food = Favorite.objects.filter(customer_id = customer.id)
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            ordered = OrderTable.objects.filter( Q(customer=customer) & Q(order_date__gt=time_now) & Q(status=True))
            is_order = False
            if ordered:
                is_order = True
            return render(request,'product/favorites.html',
                {
                'customer': request.user,
                'name': name,
                'list_favorites': list_favorites,
                'list_food': list_food,
                'ordered': ordered,
                'is_order':is_order,
                'notification':notification
                }
            )
        return render(request,'product/404.html')

    def post(self, request):
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('food_id'))#, status=True)
            favorite = Favorite.objects.filter(product_id = product.id)
            customer = Customer.objects.get(customer_id = request.user.id)
            if not favorite:
                Favorite(customer = customer, product=product).save()
            else:
                favorite.delete()
            list_favorites = Favorite.objects.filter(customer_id = customer.id).values_list('product_id', flat=True)
            return JsonResponse({"msg":"success", 'quantity':len(list_favorites)})
        else:
            return JsonResponse({"msg":"Method not allow"}, status=401)

class BookingView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not is_ajax(request):
            customer = None
            if request.user.is_authenticated:
                customer = request.user
            name, _,list_favorites,notification = getName(request)
            return render(request, 'product/booking.html',
                          {'customer':customer, 
                           'name': name, 
                           'list_favorites':list_favorites,
                           'notification':notification})
        elif is_ajax(request):
            name = request.GET.get('food-name')
            if name:
                list_product = Product.objects.filter(Q(name__istartswith= name) & Q(status=True)).order_by("name")[:30]
                content = ''
                for product in list_product:
                    pro = product.to_dict()
                    content += render_to_string('product/food-items-booking.html',
                                                {'product': pro},
                                                request=request)
                return JsonResponse({
                    "content": content
                })
            return JsonResponse({
                    "content": ""
                })

    def post(self, request, *args, **kwargs):
        try:
            booking_data = request.POST.get('booking_data')
            booking_data = json.loads(booking_data)
            booking_data['date'] = pd.to_datetime(booking_data['date'])
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            # print(booking_data['date'])
            print(booking_data['date'].weekday())
            if booking_data['date'] < time_now or (booking_data['date']- time_now).total_seconds() // 3600 > 48:
                return JsonResponse({"msg":"Your order time is not suitable!"}, status=400)
            
            if int(booking_data['noOfPeople'])==1:
                # print(booking_data['noOfPeople'])
                intend_time = (booking_data['date'] + timedelta(hours=1))
            else:
                intend_time = (booking_data['date'] + timedelta(hours=1,minutes=30))
            # print(intend_time)
            if booking_data['date'].weekday() !=6:
                # print(intend_time.hour)
                if intend_time.hour > 22 or booking_data['date'].hour < 6:
                    return JsonResponse({"msg":"Your order time is not suitable!"}, status=400)
            else:
                if intend_time.hour > 21 or booking_data['date'].hour < 9:
                    return JsonResponse({"msg":"Your order time is not suitable!"}, status=400)
            email = booking_data['email']
            phone = booking_data['phone']
            try:
                user = CustomUser.objects.get(email=email, phone_number=phone)
                customer = user.customer
                if customer.is_order:
                    return JsonResponse({"msg":"You are ordered. Please, pay for the pre-order to order!"}, status=400)
                list_order = OrderTable.objects.filter(Q(customer=customer) &Q(status=True) & Q(intend_time__gt = booking_data['date']))
                list_order = list_order.filter(Q(order_date__lt = intend_time))
                if list_order:
                    # if is_overlap(order.order_date,order.intend_time, order_table.order_date, order_table.intend_time):
                    return JsonResponse({'msg':'You are ordered. Please, choose other time!'})

                customer_is_invite = Invite.objects.filter(Q(customer=customer) & Q(end_time__gt=booking_data['date']) & Q(is_confirm=True))
                customer_is_invite = customer_is_invite.filter(Q(time_invite__lt = intend_time))
                if customer_is_invite:
                # for invit in invite_customer:
                #     if is_overlap(invit.order_detail.order_date,invit.order_detail.intend_time, order_table.order_date, order_table.intend_time):
                    return JsonResponse({'msg':'You are invited in this time. Choose other time!'})
            except:
                try:
                    new_user = CustomUser(full_name = booking_data['name'], email = email,phone_number = phone,create_not_signup=True )
                    new_user.set_password(email)
                    new_user.save()

                    customer = Customer(customer = new_user)
                    customer.save()
                except:
                    return JsonResponse({"msg":"Please, check your email or phone"}, status=400)

            type_table = TypeTable.objects.get(Q(person_per_table = int(booking_data['noOfPeople'])) & Q(status = True))
            if type_table:
                time_min = time_now + timedelta(minutes=5)
                # if (booking_data['date']- time_now).total_seconds() // 60.0 < 10:
                OrderTable.objects.filter(Q(order_date__lt=time_min) & Q(is_pending = False)).delete()

                list_table_ordered = OrderTable.objects.filter(Q(status=True) & Q(intend_time__gt = booking_data['date']) &Q(table=type_table))
                list_table_ordered = list_table_ordered.filter(Q(order_date__lt=intend_time))
                if len(list_table_ordered) < type_table.quantity:
                    order_table = OrderTable(customer= customer, order_date=booking_data['date'], table = type_table, intend_time = intend_time, special_request = booking_data['special_request'])
                    order_table.save()
                    total_money = 0
                    for key in booking_data['foods'].keys():
                        food = Product.objects.get(id = key)
                        order_food = Order(order_detail=order_table, product = food, quantity=booking_data['foods'][key]['quantity'], total_money=food.price*booking_data['foods'][key]['quantity'])
                        total_money += order_food.total_money
                        order_food.save()
                    for id in booking_data['partner']:
                        customer_invite = Customer.objects.get(id=id)
                        customer_invite_order = OrderTable.objects.filter(Q(customer=customer_invite)&Q(status=True) & Q(intend_time__gt = booking_data['date']) &Q(table=type_table))
                        customer_invite_order = customer_invite_order.filter(Q(order_date__lt=intend_time))
                        # customer_invite_order = OrderTable.objects.filter( Q(customer=customer_invite) & Q(order_date__gt=time_now) & Q(status=True))
                        # for order in customer_invite_order:
                        #     if is_overlap(order.order_date,order.intend_time, order_table.order_date, order_table.intend_time):
                        if customer_invite_order:
                            return JsonResponse({'msg':customer_invite.full_name+' had orderd in this time.'})

                        partner_is_invite = Invite.objects.filter(Q(customer=customer_invite) & Q(end_time__gt=booking_data['date']) & Q(is_confirm=True))
                        partner_is_invite = partner_is_invite.filter(Q(time_invite__lt = intend_time))
                        if partner_is_invite:
                        # invite_customer = Invite.objects.filter(Q(customer=customer_invite) & Q(time_invite__gt=time_now) & Q(is_confirm=True))
                        # for invit in invite_customer:
                        #     if is_overlap(invit.order_detail.order_date,invit.order_detail.intend_time, order_table.order_date, order_table.intend_time):
                            return JsonResponse({'msg':customer_invite.full_name+' had orderd'})
                        Invite(order_detail=order_table, customer = customer_invite, time_invite = booking_data['date']).save()

                    customer.is_order = True
                    customer.is_send_mail = False
                    customer.save()
                    order_table.total_bill = total_money
                    order_table.save()
                    Payment(order_detail=order_table, must_pay=total_money).save()
                    return JsonResponse({"msg":"success"})
            #     else:
                return JsonResponse({"msg":"table with no of people is full"}, status=400)
            return JsonResponse({"msg":"Haven't table with no of people"}, status=400)
        except:
            return JsonResponse({"msg":"OPP! Something wrong."}, status=500)

from django.template.defaultfilters import register
@register.filter()
def get_item(d, k):
    return d.get(k)

class UpdateBookingView(View):
    def get(self, request, *args, **kw):
        if request.user.is_authenticated:
            name, customer,list_favorites,notification = getName(request)
            ordered=None
            context=''
            try:
                time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
                ordered = OrderTable.objects.filter( Q(customer=customer) & Q(order_date__gt=time_now) & Q(intend_time__gt=time_now) & Q(status=True))
                list_context={}
                list_partners={}
                list_date = {}
                for order in ordered:
                    context = render_to_string('product/food_booked.html',
                                            {'ordered': order},
                                            request=request)
                    list_context[order.id] = context
                    context_partner = render_to_string('product/partner.html',
                                                        {'order_id': order.id,
                                                        'partner': order.partner.all(),
                                                        },request=request)           
                    list_partners[order.id] = context_partner
                    list_date[order.id] = order.order_date.strftime("%m/%d/%Y %H:%M")
                
                invite_accept = Invite.objects.filter(Q(customer=customer)&Q(is_confirm = True)&Q(time_invite__gt=time_now))
                list_invite_accept=[]
                for invite in invite_accept:
                    order_invite = invite.order_detail
                    list_invite_accept.append(order_invite)
                    context = render_to_string('product/food_booked.html',
                                            {'ordered': order_invite},
                                            request=request)
                    list_context[order_invite.id] = context
                    context_partner = render_to_string('product/partner.html',
                                                        {'order_id': order_invite.id,
                                                        'partner': order_invite.partner.all(),
                                                        },request=request)           
                    list_partners[order_invite.id] = context_partner
                    list_date[order_invite.id] = order_invite.order_date.strftime("%m/%d/%Y %H:%M")
                ordered_content = render_to_string('product/form_ordered.html',{
                                                    'ordered':ordered,
                                                    'list_context':list_context,
                                                    'list_date':list_date,
                                                    'order_invite': list_invite_accept,
                                                    'list_partner': list_partners,
                                                    },request=request)
                
                invites = Invite.objects.filter(Q(customer=customer)&Q(time_invite__gt = time_now)&Q(is_confirm = False))
                content_invites = render_to_string('product/invite.html',
                                                    {
                                                        'invites': invites
                                                    },request=request)
                return render(request, 'product/ordered.html',
                        {'customer':request.user,
                        'name': name,
                        'list_favorites':list_favorites,
                        'ordered':ordered_content,
                        'content_invites':content_invites,
                        'notification':notification
                        })
            except:
                return render(request, 'product/ordered.html',
                            {'customer':request.user,
                            'name': name,
                            'list_favorites':list_favorites,
                            })
        return render(request,'404.html')
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                booking_data = request.POST.get('booking_data')
                booking_data = json.loads(booking_data)
                booking_data['date'] = pd.to_datetime(booking_data['date'])
                time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

                if booking_data['date'] < time_now or (booking_data['date']- time_now).total_seconds() // 3600 > 48:
                    return JsonResponse({"msg":"Your order time is not suitable!"}, status=400)

                if booking_data['noOfPeople']==1:
                    intend_time = (booking_data['date'] + timedelta(hours=1))
                else:
                    intend_time = (booking_data['date'] + timedelta(hours=1,minutes=30))
                if booking_data['date'].weekday() !=6:
                    if intend_time.hour > 22 or booking_data['date'].hour < 6:
                        return JsonResponse({"msg":"Your order time is not suitable!"}, status=400)
                else:
                    
                    if intend_time.hour > 21 or booking_data['date'].hour < 9:
                        return JsonResponse({"msg":"Your order time is not suitable!"}, status=400)

                # customer = request.user.customer
                customer = Customer.objects.get(id = booking_data['customer_id'])

                type_table = TypeTable.objects.get(Q(person_per_table = booking_data['noOfPeople']) & Q(status = True))
                if type_table:
                    time_min = time_now + timedelta(minutes=5)
                    # if (booking_data['date']- time_now).total_seconds() // 60.0 < 10:
                    OrderTable.objects.filter(Q(order_date__lt=time_min) & Q(is_pending = False)).delete()
                    try:
                        ordered = OrderTable.objects.get(id=booking_data['id'], customer=customer)
                    except:
                        return JsonResponse({"msg":"Not found your order!"}, status=400)

                    if ordered.order_date != booking_data['date']:
                        list_order = OrderTable.objects.filter(Q(customer=customer)&Q(status=True) & Q(intend_time__gt = booking_data['date']))
                        list_order = list_order.filter(Q(order_date__lt = intend_time)).exclude(Q(id=booking_data['id']))
                        list_table_ordered = OrderTable.objects.filter(Q(status=True) & Q(intend_time__gt = booking_data['date']) &Q(table=type_table))
                        list_table_ordered = list_table_ordered.filter(Q(order_date__lt=intend_time))
                        if list_order and list_table_ordered:
                            return JsonResponse({'msg':'Please, choose other time!'})
                        ordered.order_date = booking_data['date']
                        ordered.intend_time = intend_time

                    if ordered.table.person_per_table != int(booking_data['noOfPeople']):
                        list_table_ordered = OrderTable.objects.filter(Q(status=True) & Q(intend_time__gt = booking_data['date']) &Q(table=type_table))
                        list_table_ordered = list_table_ordered.filter(Q(order_date__lt=intend_time))
                        if len(list_table_ordered) >= type_table.quantity:
                            return JsonResponse({"msg":"Table with no of people is full"}, status=400)
                        ordered.table = type_table

                    total_money = 0
                    if booking_data['foods']:
                        ordered.list_product.clear()
                        for key in booking_data['foods'].keys():
                            food = Product.objects.get(id = key)
                            order_food = Order(order_detail=ordered, product = food, quantity=booking_data['foods'][key]['quantity'], total_money=food.price*booking_data['foods'][key]['quantity'])
                            total_money += order_food.total_money
                            order_food.save()
                    if booking_data['partner']:
                        ordered.partner.clear()
                        for id in booking_data['partner']:
                            customer_invite = Customer.objects.get(id=id)
                            customer_invite_order = OrderTable.objects.filter(Q(customer=customer_invite)&Q(status=True) & Q(intend_time__gt = ordered.order_date) &Q(table=type_table))
                            customer_invite_order = customer_invite_order.filter(Q(order_date__lt=intend_time))
                            if customer_invite_order:
                                return JsonResponse({'msg':customer_invite.full_name+' had orderd in this time.'})

                            partner_is_invite = Invite.objects.filter(Q(customer=customer_invite) & Q(end_time__gt=ordered.order_date) & Q(is_confirm=True))
                            partner_is_invite = partner_is_invite.filter(Q(time_invite__lt = intend_time)).exclude(Q(order_detail=ordered))
                            if partner_is_invite:
                                return JsonResponse({'msg':customer_invite.full_name+' had orderd'})
                            Invite(order_detail=ordered, customer = customer_invite, time_invite = ordered.order_date, end_time=intend_time).save()

                    customer.is_order = True
                    customer.is_send_mail = False
                    customer.save()
                    ordered.total_bill = total_money
                    pay = ordered.payment
                    pay.must_pay = (ordered.total_bill - pay.paid) if (ordered.total_bill - pay.paid) >=0 else 0
                    if pay.must_pay > 0:
                        ordered.is_pending = False
                    pay.save()
                    ordered.save()
                    return JsonResponse({"msg":"success"})
                return JsonResponse({"msg":"Haven't table with no of people"}, status=400)
            except:
                return JsonResponse({"msg":"OPP! Something wrong."}, status=500)
        return JsonResponse({"msg":"Method not allow"}, status=401)

class DeleteBooking(View):
    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('booking_id')
            try:
                customer = request.user.customer
                ordered = OrderTable.objects.get(id=id, customer=customer)
                ordered.status = False
                ordered.save()
                time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
                ordereds = OrderTable.objects.filter( Q(customer=customer) & Q(order_date__gt=time_now) & Q(intend_time__gt=time_now) & Q(status=True))
                if ordereds:
                    check = True
                    for i in ordereds:
                        if not (i.payment.paid >0 and i.payment.mustpay ==0):
                            check = False
                    if check:
                        customer.is_order = False
                else:
                    customer.is_order = False

                customer.total_bill = ordered.payment.paid
                customer.save()
                return JsonResponse({"msg":"Success"})
            except:
                return JsonResponse({"msg":"Cancel fail"}, status=400)
        return JsonResponse({"msg":"Method not allow"}, status=401)

class PaymentView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            name, customer,list_favorites,notification = getName(request)
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            need_pay = Payment.objects.filter(Q(order_detail__customer = customer)&Q(must_pay__gt=0))
            history = Payment.objects.filter(Q(order_detail__customer = customer)&Q(must_pay=0)&Q(paid__gt=0)).order_by('-pay_date')
            try:
                discounts = DiscountBill.objects.filter(Q(start_type__lte=customer.rank.type)&Q(end_type__gte=customer.rank.type)&Q(start_date__lte=time_now)&Q(end_date__gte=time_now))
            except:
                discounts = []
            list_discount = []
            for discount in discounts:
                if not customer in discount.used_by.all():
                    list_discount.append(discount)
            # print(list_discount)
            return render(request, 'product/pay.html',
                          {'customer':request.user,
                           'name': name,
                           'list_favorites':list_favorites,
                           'history':history,
                           'need_pay':need_pay,
                           'list_discount':list_discount,
                           'notification':notification
                           })
        return render(request,'404.html')

    def post(self, request):
        if request.user.is_authenticated:
            pay = request.POST.get('id')
            discount = request.POST.get('discount')
            customer = request.user.customer
            discount_bill = None
            try:
                pay_bill = Payment.objects.get(Q(id=pay)&Q(order_detail__customer = customer))
                if discount:
                    try:
                        discount_bill = DiscountBill.objects.get(Q(id = discount))
                        if request.user in discount_bill.used_by.all():
                            return JsonResponse({"msg":"Discount not available!"}, status=404)

                    except:
                        return JsonResponse({"msg":"Discount not available!"}, status=404)
            except:
                return JsonResponse({"msg":"Pay fail!"}, status = 404)

            try:
                time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
                order = pay_bill.order_detail
                if time_now >= pay_bill.order_detail.intend_time:
                    pay_bill.status=True
                    order_food = pay_bill.order_detail.order_set.all()
                    if order_food:
                        try:
                            user_comment = Comment_product.objects.get(customer = customer)
                        except:
                            user_comment = Comment_product(customer=customer).save()
                        for food in order_food:
                            sold = ProductSold(product = food.product, sold = food.quantity)
                            user_comment.is_comment.add(food.product)
                            user_comment.food_eaten.add(food.product)
                            user_comment.save()
                            sold.save()

                    order.intend_time = time_now

                order.is_pending = True
                order.save()
                pay_bill.paid = pay_bill.must_pay
                pay_bill.must_pay = 0
                pay_bill.pay_date = time_now
                if discount:
                    discount_bill.used_by.add(customer)
                    discount_bill.save()
                customer.is_order = False
                customer.total_bill += pay_bill.paid
                customer.rank = TypeCustomer.objects.get(Q(start_money__lte=customer.total_bill)&Q(end_money__gte=customer.total_bill))
                customer.save()
                pay_bill.save()
                return JsonResponse({"msg":"Success!"})
            except:
                return JsonResponse({"msg":"Pay fail!"}, status = 400)

        return JsonResponse({"msg":"Method not allow!"}, status=401)

class InformationView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            name, _, list_favorites,notification = getName(request)
            return render(request,'product/infor.html',
                {
                'customer': request.user,
                'name': name,
                'list_favorites': list_favorites,
                'notification':notification
                }
            )
        return render(request, 'product/404.html')
    def post(self, request):
        if request.user.is_authenticated:
            data_user = request.POST.get('data_user')
            data_user = json.loads(data_user)
            # print(data_user)
            if data_user.get('password'):
                form = UpdateFormFull(data_user, instance=request.user)
            else:
                form = UpdateForm(data_user, instance=request.user)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return JsonResponse({"msg":"Success"})
            else:
                err = form.errors.get_json_data()
                msg = ''
                for val in err.values():
                    msg += val[0]['message'] + '\n'
                return JsonResponse({"msg":msg}, status=400)

        return render(request, '404.html')

class AddFoodToTablesView(View):
    def post(self, request):
        if request.user.is_authenticated:
            food_id = request.POST.get('food_id')
            quantity = request.POST.get('quantity')
            order_id = request.POST.get('order_id')
            try:
                # print(food_id)
                # print(quantity)
                # print(order_id)
                food = Product.objects.get(id=int(food_id))
                order = OrderTable.objects.get(id= int(order_id))
                if food not in order.list_product.all():
                    total_money = food.price*int(quantity)
                    Order(order_detail=order, product=food, quantity=int(quantity), total_money=total_money).save()
                    order.total_bill += total_money
                    pay = order.payment
                    pay.must_pay = (order.total_bill - pay.paid) if (order.total_bill - pay.paid) >=0 else 0
                    pay.save()
                    order.save()

                    return JsonResponse({"msg":"Success"})
                return JsonResponse({"msg":"You ordered this food."}, status=400)
            except:
                return JsonResponse({"msg":"OOP! Something errors."}, status=400)
        return JsonResponse({"msg":"Method not allowed"}, status=400)

class FoodEatenView(View):
    def get(self, request):
        if request.user.is_authenticated:
            name, customer, list_favorites,notification = getName(request)
            try:
                list_food = Comment_product.objects.get(customer = customer).food_eaten.all()
            except:
                list_food=[]
            time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            ordered = OrderTable.objects.filter( Q(customer=customer) & Q(order_date__gt=time_now) & Q(status=True))
            is_order = False
            if ordered:
                is_order = True
            return render(request,'product/food_eaten.html',
                {
                'customer': request.user,
                'name': name,
                'list_favorites': list_favorites,
                'list_food': list_food,
                'ordered': ordered,
                'is_order':is_order,
                'notification':notification
                }
            )
        return render(request,'404.html')

class ForgotPasswordView(View):
    def post(self, request):
        email = request.POST.get('email')
        if email:
            print(email)
            try:
                user = CustomUser.objects.get(email=email)
                token = RefreshToken.for_user(user).access_token
                current_site = get_current_site(request).domain
                relativeLink = reverse('product:reset-password')
                absurl='http://'+current_site+relativeLink+"?token="+str(token)
                print('reset pass: ', absurl)
                #send mail
                data = {
                    'email-subject':'Reset your password',
                    'body':'Hi '+ user.full_name+ ', use link bellow to reset your password:\n '+absurl,
                    'to_email': user.email
                }
                try:
                    Util.send_mail(data)
                except:
                    return JsonResponse({'msg':'OOP! Server is busy.Please, try again in a few minutes.'}, status=400)
                content = render_to_string('product/forgot_password.html',{'email': email})
                return JsonResponse({'content': content})
            except:
                return JsonResponse({'msg':'Your email is not exist.'}, status=400)
        return JsonResponse({'msg':'Email none'}, status=400)

class ResetPasswordView(View):
    def get(self, request):
        try:
            token = request.GET.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            customer = CustomUser.objects.get(id=payload['user_id'])
            if customer.is_active:
                return render(request, 'product/reset_password.html',{'payload': token})
            return render(request,'product/404.html')
        except jwt.ExpiredSignatureError:
            return render(request,'product/404.html')
    def post(self, request):
        try:
            token = request.POST.get('payload')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            customer = CustomUser.objects.get(id=payload['user_id'])
            if customer.is_active:
                password = request.POST.get('password')
                password2 = request.POST.get('password2')
                if len(password) < 8 or password != password2:
                    return JsonResponse({"password2":[{"message":"Password not correct format.Please, try again."}]}, status=400)
                if check_password(password, customer.password):
                    return JsonResponse({"password2":[{"message":"Password must be different old password."}]}, status=400)

                customer.set_password(password)
                customer.save()
                return JsonResponse({"msg":'Success'})
        except:
            return JsonResponse({"password2":[{"message":"OOP!Something error."}]}, status=400)

class FindPartnerView(View):
    def get(self, request):
        filter = request.GET.get('filter',None)
        try:
            customer = CustomUser.objects.get(Q(create_not_signup=False)&(Q(email=filter) | Q(phone_number=filter)))
            if request.user.is_authenticated and customer == request.user:
                return JsonResponse({'msg':'User not found.'}, status = 400)

            id = customer.customer.id
            img = customer.url_img
            full_name = customer.full_name
            return JsonResponse({'id':id,'name':full_name, 'img':img})
        except:
            return JsonResponse({'msg':'User not found.'}, status = 404)

class AcceptInviteView(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                invite_id = request.POST.get('invite_id',None)
                is_accept = request.POST.get('is_accept')
                invite = Invite.objects.get(Q(id=invite_id)&Q(customer = request.user.customer))
                if is_accept =='true':
                    if not invite.is_confirm:
                        invite.is_confirm = True
                        invite.save()
                    return JsonResponse({'msg':' Accept Successfully.'})
                if is_accept == 'false':
                    invite.delete()
                    return JsonResponse({'msg':' Reject Successfully.'})
                
                return JsonResponse({'msg':'Action fail'}, status =400)
            except:
                return JsonResponse({'msg':'Action fail'}, status =400)
        return JsonResponse({'msg':'Method not allowed'},status=401)


from django.core import serializers
class CreateDBView(View):
    def get(self, request, *args, **kwargs):
        # print( request.user.is_authenticated)
        # pro = Product.objects.filter(id__lte = 2)
        # for v in pro:
        #     print(v.product.all().values())

        # with open('category.txt', 'r') as f:
        #     data = f.read()
        # data = data.split('\n')
        # for val in data:
        #     val = json.loads(val)
        #     cate = Category(name=val['name'],decription=val['name'], url_img=val['url_img'], status=val['status'],
        #                     create_at=pd.to_datetime(val['create_at']), update_at=pd.to_datetime(val['update_at']))
        #     cate.save()


        # cate = Category.objects.get(id=1)
        # list_product = Product.objects.all()
        # with open('products_detail.txt', 'r') as f:
        #     # for category in list_product:
        #     data = f.read()
        # data = data.split('\n')
        # data.pop()
        # # val = json.loads(data[0])
        # # for v in val['img_detail'].values():
        # #     print(v)
        # for value in data:
        #     value = json.loads(value)
        #     cate = Category.objects.get(id=value['category'])
        #     try:
        #         pro = Product(name=value['name'], description=value['description'],rate=value['rate'], price=float(value['price']),
        #                     url_img=value['url_img'], category=cate, create_at=pd.to_datetime(value['create_at']),
        #                     update_at=pd.to_datetime(value['update_at']),status=value['status'])
        #         pro.save()
        #         pro = Product.objects.get(name=value['name'])
        #         for value in value['img_detail'].values():
        #             img_detail = Image_Product(product=pro, img_url=value)
        #             img_detail.save()
        #     except:
        #         pass
        return render(request, 'product/runsendmail.html')#redirect('product:home')

    def post(self, request):
        is_send = request.POST.get('is_send')
        print(is_send)
        while is_send:
            list_customer = Customer.objects.filter(is_send_mail=False)
            for customer in list_customer:
                order = OrderTable.objects.get(customer=customer, is_pending=False)
                time_now = pd.to_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
                if (order.order_date- time_now).total_seconds() // 60.0 < 20:
                    user = CustomUser.objects.get(id=customer.customer_id)
                    token = RefreshToken.for_user(customer).access_token
                    current_site = get_current_site(request).domain
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



