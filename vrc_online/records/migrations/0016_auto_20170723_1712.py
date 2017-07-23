# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0015_auto_20170723_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='horse',
            name='sale_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Sale Price'),
        ),
        migrations.AddField(
            model_name='horse',
            name='sold',
            field=models.BooleanField(default=False, verbose_name='Sold'),
        ),
    ]