from django.shortcuts import render
from product.models import Category, Product
from .models import Admin, Role
import json
from django.contrib.staticfiles.storage import staticfiles_storage
from string import digits
from django.views import View
from django.http import HttpResponse,JsonResponse
# Create your views here.


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'signin.html')

class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'signup.html')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'index.html')






















# def test_view(request, *args, **kwargs):
#     with open(staticfiles_storage.path("Thali_detail.txt")) as f:
#         data = f.read()
#     data = data.split("\n")
#     data.pop()
#     print(len(data))
#     # cate = Category.objects.get(id=5)
#     # for i in range(len(data)):
#     #     #data[i] = json.loads(data[i])
#     #     #if i>88:
#     #         val = json.loads(data[i])
#     #         remove_digits = str.maketrans('', '', digits)
#     #         val['name'] = val['name'].translate(remove_digits)
#     #         try:
#     #             rate = float(val['rate_avg'])
#     #             pro = Product(name = val['name'], description = val['name'], rate = rate, price = int(val['price'])*286, 
#     #                             url_img = val['img'], category = cate)
#     #             pro.save()
#     #         except:
#     #             rate = 3
#     #             try:
#     #                 pro = Product(name = val['name'], description = val['name'], rate = rate, price = int(val['price'])*286, 
#     #                             url_img = val['img'], category = cate)
#     #                 pro.save()
#     #             except:
#     #                 try:
#     #                     name = val['name'] + ' lut'
#     #                     pro = Product(name = name, description = val['name'], rate = rate, price = int(val['price'])*286, 
#     #                                 url_img = val['img'], category = cate)
#     #                     pro.save()
#     #                 except:
#     #                     name = val['name'] + ' lie'
#     #                     pro = Product(name = name, description = val['name'], rate = rate, price = int(val['price'])*286, 
#     #                                 url_img = val['img'], category = cate)
#     #                     pro.save()
#     # cate_list = Category.objects.filter(status='True').values()
#     return render(request, "test.html")#,{'cate_list': data}