# Generated by Django 2.2.6 on 2020-04-20 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banner_detector', '0014_auto_20200421_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='base_banner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='banner_detector.BaseBanner'),
        ),
    ]
