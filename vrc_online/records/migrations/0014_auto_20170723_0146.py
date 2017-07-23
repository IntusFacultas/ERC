# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 05:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0013_auto_20170722_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField(max_length=256, verbose_name='Details')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('horse', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='records.Horse')),
            ],
        ),
        migrations.AlterField(
            model_name='medicine',
            name='classification',
            field=models.PositiveIntegerField(blank=True, choices=[(3, 'All'), (0, 'Foals'), (1, 'Adults'), (2, 'Pregnant Mares')], null=True, verbose_name='Demographic'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='interval',
            field=models.IntegerField(blank=True, choices=[(0, 'Weeks'), (1, 'Months'), (2, 'Years')], null=True, verbose_name='Interval'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='classification',
            field=models.PositiveIntegerField(choices=[(3, 'All'), (0, 'Foals'), (1, 'Adults'), (2, 'Pregnant Mares')], verbose_name='Demographic'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='interval',
            field=models.IntegerField(choices=[(0, 'Weeks'), (1, 'Months'), (2, 'Years')], verbose_name='Interval'),
        ),
        migrations.AddField(
            model_name='medicalevent',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='records.MedicalHistory'),
        ),
    ]
