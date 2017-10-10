# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-10 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170928_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='barthel',
            name='rater',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hospitalizationinfo',
            name='bingcheng',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hospitalizationinfo',
            name='fallowupdate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='docname',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]