from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import task
from random import randint
from .models import Banner, BaseBanner
from ML_detector.core.controller import ObjectRecognitionController
import torch
import numpy as np


@shared_task
def recognize_banners(banner_ids):
    banners_descriptors = []
    banners_distance = {}
    base_banners = BaseBanner.descriptors_to_dataframe()
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


@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * randint(3, 100))
    return total
