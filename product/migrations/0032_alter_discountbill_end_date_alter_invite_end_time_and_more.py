# Generated by Django 4.1.7 on 2023-04-24 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_alter_discountbill_end_date_alter_invite_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountbill',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 24, 16, 41, 22, 368789)),
        ),
        migrations.AlterField(
            model_name='invite',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 24, 16, 41, 22, 369769)),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 24, 16, 41, 22, 369769)),
        ),
    ]
