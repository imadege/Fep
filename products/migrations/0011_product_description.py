# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
