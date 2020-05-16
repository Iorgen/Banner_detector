from __future__ import absolute_import, unicode_literals
import torch
import numpy as np
import csv
import urllib.request
import tarfile
import os
import rarfile
import re
from zipfile import ZipFile
from celery import shared_task
from .models import Banner, BaseBanner, Bus, BannerObject, BannerType, BillboardType, Billboard
from ML_detector.core.controller import ObjectRecognitionController, ObjectDetectionController
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File
from django.core.exceptions import PermissionDenied, MultipleObjectsReturned
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image


def parse_buses():
    with open('buses.csv', 'r') as f:
        reader = csv.reader(f)
        stand_type, created = BillboardType.objects.get_or_create(
            pk=0,
            defaults={'serial_number': 1, 'name': 'Стенд за водителем', 'description': 'Описание'}
        )
        print('Default stand type created')
        for row in reader:
            Bus.objects.create(
                number=row[0],
                registration_number=row[1],
                stand_id=stand_type.id
            )


def save_banner_type(tar_inputs, author):
    # TODO refactoring on temporary built-in temporary files
    BannerType.objects.all().update(active=False)
    tar_inputs.extractall(path='media/temporary_files/banner_types')
    for fn in os.listdir(os.path.join('media', 'temporary_files', 'banner_types', 'cover')):
        with open(os.path.join('media', 'temporary_files', 'banner_types', 'cover', fn), "rb") as image:
            banner_type_cover = File(image)
            banner_type, banner_type_created = BannerType.objects.get_or_create(
                name=fn[2:-4],
                defaults={
                    'image': banner_type_cover,
                    'author': author,
                    'active': True
                })
            banner_type.image = banner_type_cover
            banner_type.active = True
            banner_type.save()
    os.system('rm -rf media/temporary_files/banner_types')


@shared_task(name="Распознавание баннеров")
def recognize_banners(banner_ids):
    print('start recognize task')
    banners_descriptors = []
    banners_distance = {}
    base_banners = BaseBanner.descriptors_to_dataframe()
    base_banners_descriptors = torch.Tensor([np.array(i) for i in base_banners.banner_object__descriptor.values])
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
            banner.active = False
            # banner.banner_object.descriptor = banners_descriptors[i].tolist()
            banner.banner_object.save()
            banner.save()
        else:
            # banner.banner_object.descriptor = banners_descriptors[i].tolist()
            banner.banner_object.banner_type = target_base_banner.banner_object.banner_type
            banner.banner_object.save()
            banner.base_banner = target_base_banner
            banner.active = target_base_banner.banner_object.banner_type.active
            banner.recognition_status = True
            banner.save()
    print('finish recognize task')


@shared_task(name="пересчёт базовых дескрипторов")
def recalculate_base_banners_descriptors():
    print('start recalculate task ')
    banner_objects = BannerObject.objects.all()
    for banner_object in banner_objects:
        image = Image.open(banner_object.image.path).convert('RGB')
        banner_object.descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
        banner_object.save()
    banners_id = Banner.objects.all().values_list('id', flat=True)
    recognize_banners(banners_id)
    print('finish recalculate task')


@shared_task(name="Обновить сканы афиш")
def update_active_banner_types():
    ftpstream = urllib.request.urlopen(settings.COVERS_URL)
    inputs = tarfile.open(fileobj=ftpstream, mode="r|", encoding='cp1251')
    try:
        author = User.objects.filter(is_superuser=True).first()
        save_banner_type(inputs, author)
    except Exception:
        raise PermissionDenied()


@shared_task()
def recognize_billboards_from_rar(rar_path, user_id):
    user = User.objects.get(id=user_id)
    with ZipFile(os.path.join('media', rar_path), 'r') as billboards_zip:
        # with rarfile.RarFile(os.path.join('media', rar_path), 'r') as billboards_rar:
        for file in billboards_zip.infolist():
            if bool(re.search(".jpg", file.filename)):
                # Get image from rar file
                with transaction.atomic():
                    image_data = billboards_zip.read(file)
                    image = InMemoryUploadedFile(
                        file=BytesIO(image_data),
                        field_name=file.filename,
                        name=file.filename,
                        content_type='image/jpg',
                        size=len(image_data),
                        charset='utf-8'
                    )
                    # TODO Optimize in one regex
                    bus_tags = re.sub('Стенды/', '', file.filename)
                    bus_tags = re.sub('.jpg', '', bus_tags)

                    bus_tags = bus_tags.split('-')
                    if len(bus_tags) == 3:
                        # fixed - set unique
                        billboard_type, bt_created = BillboardType.objects.get_or_create(
                            name='Заднее стекло'
                        )
                        # fixed - set unique
                        try:
                            bus = Bus.objects.get(
                                number=bus_tags[0],
                                registration_number=bus_tags[1],
                                stand=billboard_type
                            )
                        except Bus.DoesNotExist:
                            bus = Bus.objects.create(
                                number=bus_tags[0],
                                registration_number=bus_tags[1],
                                stand=billboard_type
                            )
                        billboard = Billboard.objects.create(
                            image=image,
                            bus=bus,
                            author=user
                        )

                    elif len(bus_tags) == 2:
                        billboard_type, bt_created = BillboardType.objects.get_or_create(
                            name='Стенд за водителем'
                        )
                        # TODO this part should be in manager of BUS
                        try:
                            bus = Bus.objects.get(
                                number=bus_tags[0],
                                registration_number=bus_tags[1],
                                stand=billboard_type
                            )
                        except Bus.DoesNotExist:
                            bus = Bus.objects.create(
                                number=bus_tags[0],
                                registration_number=bus_tags[1],
                                stand=billboard_type
                            )
                        billboard = Billboard.objects.create(
                            image=image,
                            bus=bus,
                            author=user
                        )
                    banners_crops = ObjectDetectionController().banner_detection(billboard)
                    # # TODO fix костыль связанный с несовместимостью путей Django и image.ai
                    billboard.detected_image.name = os.path.join('detected_banners', billboard.image.name)
                    banner_ids = []
                    for idx, banner_crop in enumerate(banners_crops[1]):
                        # with transaction.atomic():
                        banner_object = BannerObject()
                        banner_object.image.name = banner_crop[6:]
                        image = ObjectRecognitionController().open_image(banner_object.image.path)
                        banner_object.descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
                        banner_object.save()
                        banner_object = BannerObject.objects.get(id=banner_object.id)
                        banner = Banner()
                        banner.billboard = billboard
                        banner.author = user
                        banner.banner_object = banner_object
                        banner.save()
                        banner_ids.append(banner.id)
                    recognize_banners(banner_ids=banner_ids)
                    billboard.save()
    os.system('rm -rf ' + os.path.join('media', rar_path))
