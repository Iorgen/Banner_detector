# Generated by Django 2.2.6 on 2019-12-09 15:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner_detector', '0004_auto_20191207_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerobject',
            name='descriptor',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[1, 2, 3], size=None),
            preserve_default=False,
        ),
    ]
