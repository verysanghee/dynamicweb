# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-06 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0034_auto_20170504_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmachineplan',
            name='opennebula_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]