# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-17 13:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_outlet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='outlet',
        ),
    ]