# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_auto_20161102_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardswipe',
            name='identifier',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
