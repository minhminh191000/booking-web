# Generated by Django 4.1.7 on 2023-04-11 16:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_ordertable_is_payment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discountbill',
            name='times',
        ),
        migrations.AddField(
            model_name='customer',
            name='rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.typecustomer'),
        ),
        migrations.AddField(
            model_name='discountbill',
            name='used_by',
            field=models.ManyToManyField(blank=True, related_name='used_discountbill', to='product.customer'),
        ),
        migrations.AlterField(
            model_name='discountbill',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 11, 17, 31, 51, 66697)),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 11, 17, 31, 51, 71704)),
        ),
        migrations.DeleteModel(
            name='RankCustomer',
        ),
    ]
