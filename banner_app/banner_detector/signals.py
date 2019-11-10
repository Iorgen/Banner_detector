from django.db.models.signals import post_save
from .models import BillboardImage, Banner
from django.dispatch import receiver


# @receiver(post_save, sender=BillboardImage)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         xsum(4)
