# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-10 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import letters.models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0005_auto_20170210_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='file',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to=letters.models.upload_path_handler),
        ),
    ]