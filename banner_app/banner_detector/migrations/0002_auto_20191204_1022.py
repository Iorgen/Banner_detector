# Generated by Django 2.2.6 on 2019-12-04 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banner_detector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='base_banner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='banner_detector.BaseBanner'),
        ),
    ]
