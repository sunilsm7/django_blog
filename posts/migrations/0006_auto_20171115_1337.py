# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20171114_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(),
        ),
    ]
