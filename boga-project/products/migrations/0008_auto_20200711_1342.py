# Generated by Django 3.0.7 on 2020-07-11 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_closing_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='closing_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 11, 13, 42, 42, 758767)),
        ),
    ]