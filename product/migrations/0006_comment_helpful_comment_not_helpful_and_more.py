# Generated by Django 4.1.7 on 2023-04-05 02:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_customer_is_order_alter_ordertable_intend_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='helpful',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='not_helpful',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 5, 3, 32, 4, 535889, tzinfo=datetime.timezone.utc)),
        ),
    ]
