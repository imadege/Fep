# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20161204_0014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['date_created']},
        ),
        migrations.RemoveField(
            model_name='unit',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.Unit'),
            preserve_default=False,
        ),
    ]
