# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlets', '0001_initial'),
        ('products', '0014_product_outlet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='outlet',
        ),
        migrations.AddField(
            model_name='product',
            name='outlet',
            field=models.ManyToManyField(to='outlets.Outlet'),
        ),
    ]
