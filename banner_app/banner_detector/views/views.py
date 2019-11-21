from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from ..forms import ImportBaseBannersForm, BaseBannerCreationForm
from ..models import BaseBanner, BannerType
from ML_detector.core.controller import ObjectRecognitionController
import os
import re
from zipfile import ZipFile
from PIL import Image
from io import BytesIO, StringIO
import sys


# Create your views here.
def home(request):
    context = {
        'title': 'Banner_detector',
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
            print(os.getcwd())
            with ZipFile(request.FILES['archive_file'], 'r') as banners_zip:
                dirs = list(set([os.path.dirname(x) for x in banners_zip.namelist()]))
                banner_types = [os.path.split(x)[1] for x in dirs]
                for banner_type_name in banner_types:
                    banner_type, banner_type_created = BannerType.objects.get_or_create(
                        name=banner_type_name,
                        defaults={'author': request.user}
                    )
                    # Compare with banner_type object in base using get_or_create() method
                    print('-------------------')
                    for info in banners_zip.infolist():
                        template_name = re.compile('data/' + banner_type_name + '/.*\.jpg')
                        # Get descriptop
                        # compare descriptors if distacne < 0.5 add to database
                        if re.match(template_name, info.filename):
                            base_banner_form = BaseBannerCreationForm()
                            image_data = banners_zip.read(info.filename)
                            # image_data = BytesIO(image_data)
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
                            base_banner, base_banner_created = BaseBanner.objects.get_or_create(
                                descriptor=descriptor, defaults={
                                    'author': request.user,
                                    'image': image,
                                    'banner_type': banner_type,
                                    'descriptor': descriptor
                            })
                            print(info.filename)
                # images = banners_zip.read('data/салон_измерительной_техники_измертех/*.jpg')
                # print(images)
            messages.add_message(self.request, messages.INFO, 'Базовые баннеры успешно занесены, список типов расширен')
            return redirect(reverse('detector-home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, 'banner_detector/import_base_banners.html', {'form': form})
