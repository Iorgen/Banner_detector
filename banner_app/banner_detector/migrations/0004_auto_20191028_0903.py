# Generated by Django 2.2.6 on 2019-10-28 09:03

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banner_detector', '0003_auto_20191027_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerBaseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='default.jpg', upload_to='banner_classes')),
                ('descriptor', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BannerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='banner',
            name='name',
        ),
        migrations.AddField(
            model_name='banner',
            name='recognition_status',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='BannerClass',
        ),
        migrations.AddField(
            model_name='bannerbaseimage',
            name='banner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner_detector.BannerType'),
        ),
        migrations.AddField(
            model_name='banner',
            name='banner_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='banner_detector.BannerType'),
        ),
    ]