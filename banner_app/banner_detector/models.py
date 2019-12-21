import pandas as pd
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.template.loader import render_to_string
from .managers import BannerManager


class Bus(models.Model):
    """
    Stores a single bus entry.
    """
    number = models.CharField(max_length=20, default="1")
    registration_number = models.CharField(max_length=20, default="1")

    def __str__(self):
        return self.number + '-' + self.registration_number


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
        return "Биллборд в '" + self.bus.number + "' за " + self.day_month_added()

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

    def banners_count(self):
        """
        :return: int()
        """
        return Banner.objects.filter(billboard_id=self.pk).count()

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


class BannerType(models.Model):
    """
    Stores a information about single unique banner type(class) entry,
    related to :model:`auth.User`.
    """
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='covers')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BannerObject(models.Model):
    """

    """
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='banners')
    descriptor = ArrayField(models.FloatField(), null=False)
    banner_type = models.ForeignKey(BannerType, on_delete=models.CASCADE, blank=True, null=True)


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
    base_banner = models.ForeignKey(BaseBanner, on_delete=models.CASCADE, blank=True, null=True)
    objects = BannerManager()
