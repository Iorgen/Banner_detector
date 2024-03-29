import pandas as pd
import torch
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.template.loader import render_to_string
from django.conf import settings
from .managers import BannerManager
from datetime import date


class BillboardType(models.Model):
    """ Store information about billboard type (for bus side)"""
    serial_number = models.IntegerField(default=1, unique=True)
    name = models.CharField(max_length=20, default="Название", unique=True)
    description = models.CharField(max_length=100, default="Описание", unique=True)

    def __str__(self):
        return f'Тип Стенда номер{self.serial_number}-{self.description}'


class Bus(models.Model):
    """
    Stores a single bus entry.
    """
    number = models.CharField(max_length=20, default="1")
    registration_number = models.CharField(max_length=20, default="1")
    stand = models.ForeignKey(BillboardType, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.stand.name == 'Стенд за водителем':
            return f'{self.number}-{self.registration_number}'
        else:
            return f'{self.number}-{self.registration_number}-{self.stand.serial_number}'

    @property
    def today_billboards(self):
        today = date.today()
        current_bus_billboards = Billboard.objects.filter(date_added__year=today.year,
                                                          date_added__month=today.month,
                                                          date_added__day=today.day,
                                                          bus_id=self.pk)
        return current_bus_billboards

    def interval_billboards(self, datetime_from, datetime_to):
        return Billboard.objects.filter(
            date_added__lte=datetime_to,
            date_added__gte=datetime_from,
            bus_id=self.pk
        )


class Billboard(models.Model):
    """
    Stores a information about single billboard entry,
    related to :model:`banner_detector.Bus` and :model:`auth.User`.
    """
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='billboards')
    detected_image = models.ImageField(default='default.jpg', upload_to='billboards')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return "Стенд в '" + self.bus.registration_number + "' за " + self.day_month_added()

    def get_absolute_url(self):
        return reverse('billboard-detail', kwargs={'pk': self.pk})

    def day_month_added(self):
        """ in which time sample was added in 'day month' format
        :return: str()
        """
        return self.date_added.strftime("%d.%m")

    def get_not_classified_banners(self):
        """

        :return: int()
        """
        not_classified_banners = Banner.objects.filter(billboard__id=self.pk, banner_object__banner_type=None)
        return len(not_classified_banners)

    def get_recognized_banners(self):
        """
        :return: int()
        """
        not_classified_banners = Banner.objects.filter(billboard__id=self.pk, recognition_status=True)
        return len(not_classified_banners)

    def export_xml(self):
        """

        :return:
        """
        banner = Banner.objects.filter(billboard_id=self.pk)
        xml = render_to_string('banner_detector/banner_info.xml',
                               {'banners': banner, 'billboard': self})
        return xml

    def get_formatted(self):
        return self.date_added.strftime("%Y-%m-%dT%H:%M:%S")

    @property
    def get_banners(self):
        return Banner.objects.filter(billboard=self)

    @property
    def banners_count(self):
        """
        :return: int()
        """
        return Banner.objects.filter(billboard_id=self.pk).count()

    @property
    def number_of_trash_posters(self):
        trash_type = BannerType.objects.filter(name=settings.GARBAGE_BANNER_TYPE).first()
        return Banner.objects.filter(billboard_id=self.pk, banner_object__banner_type_id=trash_type.id).count()

    @property
    def number_of_social_posters(self):
        social_type = BannerType.objects.filter(name=settings.SOCIAL_BANNER_TYPE).first()
        return Banner.objects.filter(billboard_id=self.pk, banner_object__banner_type_id=social_type.id).count()


class BannerType(models.Model):
    """
    Stores a information about single unique banner type(class) entry,
    related to :model:`auth.User`.
    """
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_poster.jpg', upload_to='covers')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BannerObject(models.Model):
    """

    """
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='banners')
    descriptor = ArrayField(models.FloatField(), null=False)
    banner_type = models.ForeignKey(BannerType, on_delete=models.SET_NULL, blank=True, null=True)


class BaseBanner(models.Model):
    """
    Stores a information about single banner entry
    related to :model:'auth.User', :model:'banner_detector.BannerType'.
    """

    banner_object = models.OneToOneField(BannerObject, on_delete=models.CASCADE, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    # TODO Move to custom manager
    @staticmethod
    def descriptors_to_dataframe():
        """
        Convert all base banners into pandas.DataFrame format
        :return: pandas.DataFrame()
        """
        base_banners = pd.DataFrame(list(
            BaseBanner.objects.all().values('id', 'banner_object__descriptor')
        ))
        return base_banners

    def get_absolute_url(self):
        return reverse('base-banner-detail', kwargs={'pk': self.pk})

    def day_month_added(self):
        """ in which time sample was added in 'day month' format
        :return: str()
        """
        return self.date_added.strftime("%d.%m")


class Banner(models.Model):
    """
    Stores a information about single banner entry
    related to :model:'banner_detector.BannerType', :model:'banner_detector.BillboardImage'
    recognition status True - recognized, False - never recognized
    """
    banner_object = models.OneToOneField(BannerObject, on_delete=models.CASCADE, unique=True)
    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    recognition_status = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    distance = models.FloatField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    base_banner = models.ForeignKey(BaseBanner, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)
    objects = BannerManager()

    def save(self, *args, **kwargs):
        if (self.base_banner is not None) and \
                (self.banner_object is not None):
            self.distance = torch.pairwise_distance(
                torch.FloatTensor(self.banner_object.descriptor),
                torch.FloatTensor([self.base_banner.banner_object.descriptor])
            ).cpu().numpy()[0]
            self.active = self.base_banner.banner_object.banner_type.active
        super(Banner, self).save(*args, **kwargs)
