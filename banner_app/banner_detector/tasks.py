from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Banner, BaseBanner, Bus, BannerObject
from PIL import Image
from ML_detector.core.controller import ObjectRecognitionController
import torch
import numpy as np
import csv


@shared_task
def recognize_banners(banner_ids):
    print('inside task')
    print(banner_ids)
    banners_descriptors = []
    banners_distance = {}
    base_banners = BaseBanner.descriptors_to_dataframe()
    # TODO empty BaseBanners handler
    base_banners_descriptors = torch.Tensor([np.array(i) for i in base_banners.banner_object__descriptor.values])
    print('after descriptors')
    for i, banner_id in enumerate(banner_ids):
        # Comment
        banner = Banner.objects.get(pk=banner_id)
        image = ObjectRecognitionController().open_image(banner.banner_object.image.path)
        banners_descriptors.append(ObjectRecognitionController().get_descriptor(image))
        banners_distance[banner_id] = torch.pairwise_distance(banners_descriptors[i],
                                                              base_banners_descriptors).cpu().numpy()
        # Comment
        distance = list(banners_distance[banner_id])
        banner.distance = sorted(distance)[0]
        most_similar_base_banner_index = distance.index(sorted(distance)[0])
        target_class_id = base_banners['id'][most_similar_base_banner_index]
        target_base_banner = BaseBanner.objects.get(pk=target_class_id.item())
        print(sorted(distance)[0])

        # Check distance
        if sorted(distance)[0] > ObjectRecognitionController.distance_threshold:
            print('не распознан')
            banner.recognition_status = True
            # banner.banner_object.descriptor = banners_descriptors[i].tolist()
            banner.banner_object.save()
            banner.save()
        else:
            # banner.banner_object.descriptor = banners_descriptors[i].tolist()
            banner.banner_object.banner_type = target_base_banner.banner_object.banner_type
            banner.banner_object.save()
            banner.base_banner = target_base_banner
            banner.recognition_status = True
            banner.save()


@shared_task
def recalculate_base_banners_descriptors():
    banner_objects = BannerObject.objects.all()
    for banner_object in banner_objects:
        image = Image.open(banner_object.image.path).convert('RGB')
        banner_object.descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
        banner_object.save()
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
