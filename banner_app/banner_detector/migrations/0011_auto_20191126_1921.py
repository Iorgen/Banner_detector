# Generated by Django 2.2.6 on 2019-11-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner_detector', '0010_auto_20191126_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='number',
            field=models.CharField(default='1', max_length=20),
        ),
    ]
