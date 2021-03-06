# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 18:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_business_is_deleted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0017_auto_20170103_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('commission', models.IntegerField(help_text='% age commission for calculating selling price ')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
