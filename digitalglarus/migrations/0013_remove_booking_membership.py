# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-30 04:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalglarus', '0012_booking_free_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='membership',
        ),
    ]