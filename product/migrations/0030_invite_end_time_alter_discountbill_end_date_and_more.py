# Generated by Django 4.1.7 on 2023-04-19 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_alter_discountbill_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 19, 22, 6, 22, 344739)),
        ),
        migrations.AlterField(
            model_name='discountbill',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 19, 22, 6, 22, 343743)),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 19, 22, 6, 22, 344739)),
        ),
    ]
