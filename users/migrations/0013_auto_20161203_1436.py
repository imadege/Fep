# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 11:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20161203_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_time_created',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
    ]
