from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from user.models import CustomUser

# Create your models here.
def intend_time():
    return timezone.now() + timezone.timedelta(hours=1, minutes=30)

class TypeCustomer(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    type = models.IntegerField(unique=True, blank=False, null=False)
    start_money = models.DecimalField(max_digits = 15,decimal_places = 3)
    end_money = models.DecimalField(max_digits = 15,decimal_places = 3)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'type_customer'

class Customer(models.Model):
    customer = models.OneToOneField(CustomUser, related_name='customer', on_delete=models.CASCADE) 
    is_send_mail = models.BooleanField(default=True)
    is_order = models.BooleanField(default=False)
    total_bill = models.DecimalField(default=0,max_digits = 12,decimal_places = 3)
    rank = models.ForeignKey(TypeCustomer, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return "Customer id: "+str(self.id)

    class Meta:
        db_table = 'customer'

# class RankCustomer(models.Model):
#     customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     type_customer = models.ForeignKey(TypeCustomer, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'rank_customer'
#         unique_together = ['customer', 'type_customer']


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    decription = models.CharField(max_length=255, blank=False, null=False)
    url_img = models.TextField()
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(default= timezone.now)
    update_at = models.DateTimeField()

    def to_dict(self):
        return{
            "name": self.name,
            "decription": self.decription,
            "url_img": self.url_img,
            "status": self.status,
            "create_at": str(self.create_at),
            "update_at": str(self.update_at)
        }

    class Meta:
        db_table = 'category'
from django.core import serializers

class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    rate = models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    price = models.DecimalField(max_digits = 10,decimal_places = 3)
    url_img = models.TextField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'product'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # "description": self.description,
            "rate": self.rate,
            "price": str(self.price),
            "url_img": self.url_img,
            # "category": self.category.id,
            # "create_at": str(self.create_at),
            # "update_at": str(self.update_at),
            # "status": str(self.status)
        }
    
    # def extra_img(self):
    #     return serializers.serialize('python', self.product.all())

class ProductSold(models.Model):
    product = models.OneToOneField(Product, related_name='product_sold', on_delete=models.CASCADE)
    sold = models.IntegerField(default=0)

    class Meta:
        db_table = "product_sold"
    
class Image_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    img_url = models.TextField()
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'image_product'

class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment_date = models.DateTimeField(default=timezone.now)
    helpful = models.IntegerField(default=0)
    user_helpful = models.ManyToManyField(Customer, blank=True, related_name='user_helpful')
    not_helpful = models.IntegerField(default=0)
    user_not_helpful = models.ManyToManyField(Customer, blank=True, related_name='user_not_helpful')

    
    class Meta:
        db_table = 'comment'

class Comment_product(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    is_comment = models.ManyToManyField(Product, blank=True)
    food_eaten = models.ManyToManyField(Product, blank=True,related_name='food_eaten')

    class Meta:
        db_table = 'user_comment'

class Discount(models.Model):
    sell_off = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'discount'

class DiscountBill(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    sell_off = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    start_type = models.IntegerField(default=1)
    end_type = models.IntegerField(default=1)
    # special_customer = models.ForeignKey(Cus)
    # times = models.IntegerField(default=1)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=intend_time())
    used_by = models.ManyToManyField(Customer, related_name='used_discountbill', blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'discount_bill'

class TypeTable(models.Model):
    person_per_table = models.IntegerField(default=1, unique=True, blank=False, null=False)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'type_table'

# class Table(models.Model):
#     type_table = models.ForeignKey(TypeTable, related_name='type_table', on_delete=models.CASCADE)
#     status = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         db_table = 'table'

class OrderTable(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(default=timezone.now)
    table = models.ForeignKey(TypeTable, related_name='table', on_delete=models.DO_NOTHING)
    intend_time = models.DateTimeField(default=intend_time())
    special_request = models.TextField(default=None, blank=True, null=True)
    list_product = models.ManyToManyField(Product,through='Order')
    is_pending = models.BooleanField(default=False)
    # is_payment = models.BooleanField(default=False)
    total_bill = models.DecimalField(default=0, validators=[MinValueValidator(0)],max_digits = 10,decimal_places = 3)
    status = models.BooleanField(default=True)
    partner = models.ManyToManyField(Customer, related_name='partner',through='Invite')

    class Meta:
        db_table = 'order_table'

class Order(models.Model):
    order_detail = models.ForeignKey(OrderTable, on_delete=models.CASCADE, db_column='order_table')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    special_request = models.TextField(default=None, blank=True, null=True)
    total_money = models.DecimalField(default=0, validators=[MinValueValidator(0)],max_digits = 10,decimal_places = 3)

    class Meta:
        db_table = 'order'
        unique_together = ['order_detail', 'product']
    
class Invite(models.Model):
    order_detail = models.ForeignKey(OrderTable, on_delete=models.CASCADE, db_column='order_table')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer')
    time_invite = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=intend_time())
    is_confirm = models.BooleanField(default=False)
    class Meta:
        db_table = 'invite'

class Payment(models.Model):
    order_detail = models.OneToOneField(OrderTable, on_delete=models.CASCADE)
    pay_date = models.DateTimeField(blank=True, null=True)
    paid = models.DecimalField(max_digits = 10,decimal_places = 3, default=0)
    must_pay = models.DecimalField(max_digits = 10,decimal_places = 3, default=0)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'payment'

class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'favorite'
        unique_together = ['customer', 'product']


# class Restaurant(models.Model):
#     customer = models.ForeignKey(Customer, related_name='customer_id', on_delete=models.CASCADE)
#     type_table = models.ForeignKey(TypeTable, related_name='person_type_table', on_delete=models.CASCADE)
#     order = models.ForeignKey(OrderDetail, related_name='order_id', on_delete=models.CASCADE)
#     intend_time = models.DateTimeField(default=intend_time()) 

#     class Meta:
#         db_table = 'restaurant'

from django.contrib import admin
admin.site.register([TypeCustomer,Customer,Category,Product,ProductSold,
                     Image_Product,Comment,Comment_product,Discount,DiscountBill,TypeTable,
                     OrderTable,Order,Invite,Payment,Favorite])