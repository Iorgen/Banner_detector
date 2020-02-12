import os
import re
import tarfile
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from ..forms import ImportBaseBannersForm, ImportBannersTypesForm
from ..models import BaseBanner, BannerType, BannerObject, Banner, Billboard, Bus
from ..tasks import save_banner_type, update_active_banner_types, recalculate_base_banners_descriptors
from ML_detector.core.controller import ObjectRecognitionController
from users.models import Profile
from zipfile import ZipFile
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta, date
from django_celery_results.models import TaskResult


def home(request):
    today = date.today()
    today_billboards = Billboard.objects.filter(date_added__year=today.year,
                                                date_added__month=today.month,
                                                date_added__day=today.day).count()

    context = {
        'title': 'Banner_detector',
        'number_of_base_banners': BaseBanner.objects.count(),
        'number_of_billboards': Billboard.objects.count(),
        'number_of_banners': Banner.objects.count(),
        'number_of_banner_objects': BannerObject.objects.count(),
        'number_of_buses': Bus.objects.count(),
        'number_of_workers': User.objects.filter(groups__name__contains='worker').count(),
        # Today information
        'today_billboards': today_billboards,
        # Users
        'profiles': Profile.objects.all(),
        'background_tasks_results': TaskResult.objects.all()
    }
    return render(request, 'banner_detector/home.html', context)


class ImportBaseBanners(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    form_class = ImportBaseBannersForm
    permission_required = 'banner_detector.add_basebanner'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'banner_detector/import_base_banners.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            with ZipFile(request.FILES['archive_file'], 'r') as banners_zip:
                dirs = list(set([os.path.dirname(x) for x in banners_zip.namelist()]))
                banner_types = [os.path.split(x)[1] for x in dirs]
                for banner_type_name in banner_types:
                    with transaction.atomic():
                        banner_type, banner_type_created = BannerType.objects.get_or_create(
                            name=banner_type_name,
                            defaults={'author': request.user}
                        )
                        for info in banners_zip.infolist():
                            template_name = re.compile('data/' + banner_type_name + r'/.*\.jpg')
                            if re.match(template_name, info.filename):
                                image_data = banners_zip.read(info.filename)
                                image = InMemoryUploadedFile(
                                    file=BytesIO(image_data),
                                    field_name=info.filename,
                                    name=info.filename,
                                    content_type='image/jpeg',
                                    size=len(image_data),
                                    charset='utf-8'
                                )

                                base_banner_image = Image.open(image).convert('RGB')
                                descriptor = ObjectRecognitionController().get_descriptor(base_banner_image).tolist()
                                banner_object, banner_object_created = BannerObject.objects.get_or_create(
                                    descriptor=descriptor,
                                    defaults={
                                        'image': image,
                                        'banner_type': banner_type,
                                    }
                                )
                                base_banner, base_banner_created = BaseBanner.objects.get_or_create(
                                    banner_object=banner_object,
                                    defaults={
                                        'author': request.user,
                                    })
            messages.add_message(self.request, messages.INFO, 'Базовые баннеры успешно занесены, список типов расширен')
            return redirect(reverse('detector-home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, 'banner_detector/import_base_banners.html', {'form': form})


class ImportBannersTypesFromFile(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    form_class = ImportBannersTypesForm
    permission_required = 'banner_detector.add_bannertype'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'banner_detector/import_base_banners.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            inputs = tarfile.open(fileobj=request.FILES['archive_file'], mode="r|", encoding='cp1251')
            save_banner_type(inputs, request.user)
            messages.add_message(self.request, messages.INFO, 'Типы баннеров занесены, активность типов обновлена')
            return redirect(reverse('detector-home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, 'banner_detector/import_base_banners.html', {'form': form})
