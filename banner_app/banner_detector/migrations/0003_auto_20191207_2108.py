# Generated by Django 2.2.6 on 2019-12-07 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banner_detector', '0002_auto_20191204_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner_detector.BannerObject', unique=True),
        ),
        migrations.AlterField(
            model_name='basebanner',
            name='banner_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner_detector.BannerObject', unique=True),
        ),
    ]
