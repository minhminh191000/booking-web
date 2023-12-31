# Generated by Django 4.1.7 on 2023-04-12 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_alter_discountbill_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertable',
            name='is_payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discountbill',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 12, 17, 51, 39, 342443)),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 12, 17, 51, 39, 342443)),
        ),
    ]
