# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
        ('orders', '0010_delete_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bill', to='bills.Bill'),
        ),
    ]
