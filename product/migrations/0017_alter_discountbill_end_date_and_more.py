# Generated by Django 4.1.7 on 2023-04-12 15:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_ordertable_status_alter_discountbill_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountbill',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 12, 16, 48, 29, 755815)),
        ),
        migrations.AlterField(
            model_name='discountbill',
            name='type_customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='typecustomer', to='product.typecustomer'),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 12, 16, 48, 29, 756815)),
        ),
    ]
