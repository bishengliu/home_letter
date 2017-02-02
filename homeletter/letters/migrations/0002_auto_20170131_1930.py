# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-31 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='letter',
            old_name='letter_file',
            new_name='file_path',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='letter_date',
        ),
        migrations.AddField(
            model_name='letter',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='letter',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]