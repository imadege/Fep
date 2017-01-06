# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20161219_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AddField(
            model_name='price',
            name='commission',
            field=models.IntegerField(default=23, help_text='% age commission for calculating selling price '),
            preserve_default=False,
        ),
    ]