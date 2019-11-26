from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Banner, BaseBanner, Bus
from PIL import Image
from ML_detector.core.controller import ObjectRecognitionController
import torch
import numpy as np
import os
import csv


@shared_task
def recognize_banners(banner_ids):
    banners_descriptors = []
    banners_distance = {}
    base_banners = BaseBanner.descriptors_to_dataframe()
    # TODO empty BaseBanners handler
    print(base_banners.head(10))
    base_banners_descriptors = torch.Tensor([np.array(i) for i in base_banners.descriptor.values])
    # Count descriptors for income images (classified)
    for i, banner_id in enumerate(banner_ids):
        # Comment
        banner = Banner.objects.get(pk=banner_id)
        image = ObjectRecognitionController().open_image(banner.image.path)
        banners_descriptors.append(ObjectRecognitionController().get_descriptor(image))
        banners_distance[banner_id] = torch.pairwise_distance(banners_descriptors[i],
                                                              base_banners_descriptors).cpu().numpy()
        # Comment
        distance = list(banners_distance[banner_id])
        banner.closest_distance = sorted(distance)[0]
        most_similar_base_banner_index = distance.index(sorted(distance)[0])
        target_class_id = base_banners['id'][most_similar_base_banner_index]
        target_base_banner = BaseBanner.objects.get(pk=target_class_id.item())
        print(sorted(distance)[0])

        # Check distance
        if sorted(distance)[0] > 38:
            print('не распознан')
            banner.recognition_status = True
            banner.save()
        else:
            banner.banner_class = target_base_banner.banner_type
            banner.recognition_status = True
            banner.save()


@shared_task
def recalculate_descriptors():
    base_banners = BaseBanner.objects.all()
    for base_banner in base_banners:
        image = Image.open(base_banner.image.path).convert('RGB')
        base_banner.descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
        base_banner.save()
    banners_id = Banner.objects.all().values_list('id', flat=True)
    recognize_banners(banners_id)


def parse_buses():
    with open('output.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            Bus.objects.create(
                number=row[0],
                registration_number=row[1]
            )
