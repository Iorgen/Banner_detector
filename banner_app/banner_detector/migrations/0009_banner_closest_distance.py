# Generated by Django 2.2.6 on 2019-11-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner_detector', '0008_auto_20191101_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='closest_distance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
