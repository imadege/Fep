# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161203_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_level',
            field=models.IntegerField(help_text='No. of products in store'),
        ),
    ]
