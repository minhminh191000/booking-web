# Generated by Django 4.1.7 on 2023-03-31 07:18

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_orderdetail_intend_time_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='intend_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 31, 8, 18, 0, 486505, tzinfo=datetime.timezone.utc)),
        ),
    ]
