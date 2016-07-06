# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waveforms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapping',
            name='file_regex',
        ),
        migrations.RemoveField(
            model_name='mapping',
            name='path_regex',
        ),
        migrations.AddField(
            model_name='continuoustrace',
            name='original_channel',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AddField(
            model_name='continuoustrace',
            name='original_location',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='continuoustrace',
            name='original_network',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='continuoustrace',
            name='original_station',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='mapping',
            name='full_path_regex',
            field=models.CharField(default='.*', max_length=255),
        ),
        migrations.AlterField(
            model_name='mapping',
            name='channel',
            field=models.CharField(blank=True, db_index=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='mapping',
            name='location',
            field=models.CharField(blank=True, db_index=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='mapping',
            name='network',
            field=models.CharField(blank=True, db_index=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='mapping',
            name='station',
            field=models.CharField(blank=True, db_index=True, max_length=5),
        ),
    ]
