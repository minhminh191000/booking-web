from time import timezone
import pandas as pd
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from typing import Mapping, Any, List, Dict
from .models import Category, Product, Image_Product, Customer, CustomUser, Favorite, TypeTable, OrderTable, \
    Order, Payment, ProductSold,DiscountBill, TypeCustomer, Comment_product, Comment, Invite


class PorductProduct:

    def get_data_test(self):
        vals = [{"name": "Soburnb",
                "description": "snoffe is a product",
                "rate": 2.0,
                "price": 100000,
                "url_img": None,
                "status": True,
                }]

    def _get_vals(self, name= None, description= None, rate= None, price= None, url_img= None, category= None, status= True):
        vals = {'name': name,
                'description': description,
                'rate': rate,
                'price': price,
                'url_img': url_img,
                'category': category,
                'status': status,
                }

    @classmethod
    def create_product(cls, products: List[Product]):
        """
        
        Create a new product
        """
    
        data = []
        if products:
            for product in products:
                # product_model = model_to_dict(product)
                data_set = Product(
                    name= product.get('name'),
                    description= product.get('description'),
                    rate= product.get('rate'),
                    price= product.get('price'),
                    url_img= product.get('url_img'),
                    category_id= product.get('category_id'),
                    status= product.get('status'),
                
                )
                data.append(data_set)
            Product.objects.bulk_create(data)
            return True
        else:
            return False