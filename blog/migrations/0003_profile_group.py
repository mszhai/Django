# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-04 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='group',
            field=models.CharField(default='doctor', max_length=200),
        ),
    ]
