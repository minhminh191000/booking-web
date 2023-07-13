# Generated by Django 4.1.7 on 2023-04-15 09:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_comment_product_food_eaten_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_helpful',
            field=models.ManyToManyField(blank=True, related_name='user_helpful', to='product.customer'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_not_helpful',
            field=models.ManyToManyField(blank=True, related_name='user_not_helpful', to='product.customer'),
        ),
        migrations.AlterField(
            model_name='discountbill',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 15, 10, 33, 15, 227962)),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 15, 10, 33, 15, 227962)),
        ),
    ]