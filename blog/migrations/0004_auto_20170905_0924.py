# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-05 01:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_profile_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalizationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospitno_fk', models.CharField(max_length=50)),
                ('evaluate_status', models.IntegerField(default=1)),
                ('patid_fk', models.CharField(blank=True, max_length=50)),
                ('entdate', models.DateTimeField(blank=True)),
                ('outdate', models.DateTimeField(blank=True)),
                ('dignose', models.CharField(max_length=50)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='PatientInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patid_fk', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('birthday', models.DateTimeField(blank=True)),
                ('sex', models.CharField(blank=True, max_length=2)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='hospitalizationinfo',
            name='patid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.PatientInfo'),
        ),
    ]
