# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-13 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170905_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barthel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluate_time', models.DateTimeField(auto_now=True)),
                ('dabian', models.IntegerField()),
                ('xiaobian', models.IntegerField()),
                ('xiushi', models.IntegerField()),
                ('yongce', models.IntegerField()),
                ('chifan', models.IntegerField()),
                ('zhuanyi', models.IntegerField()),
                ('huodong', models.IntegerField()),
                ('chuanyi', models.IntegerField()),
                ('louti', models.IntegerField()),
                ('xizao', models.IntegerField()),
                ('total_score', models.IntegerField()),
                ('times', models.IntegerField()),
                ('hospid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.HospitalizationInfo')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Profile')),
            ],
        ),
    ]
