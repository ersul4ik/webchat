# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20171207_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='seen',
            field=models.BooleanField(default=True),
        ),
    ]
