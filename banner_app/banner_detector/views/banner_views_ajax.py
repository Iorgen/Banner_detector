from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import Banner, BannerType, BaseBanner
from django.views.generic import (View)
from ML_detector.core.controller import ObjectRecognitionController
from PIL import Image


class BannerCreateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.change_banner'

    def post(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = Banner.objects.create(
            name=name1,
            address=address1,
            age=age1
        )

        user = {'id': obj.id, 'name': obj.name,
                'address': obj.address, 'age': obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)


class BannerUpdateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.change_banner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        banner_type_name = request.GET.get('banner_type_name', None)
        banner = Banner.objects.get(id=banner_id)
        banner_type, created = BannerType.objects.get_or_create(name=banner_type_name, defaults={'author': request.user})
        banner.banner_class = banner_type
        banner.recognition_status = True
        banner.save()
        image = Image.open(banner.image.path).convert('RGB')
        descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
        # create base banner instance
        BaseBanner.objects.create(
            author=request.user,
            image=banner.image.name,
            descriptor=descriptor,
            banner_type_id=banner.banner_class_id,
        )
        banner = {'id': banner.id, 'banner_type': banner.banner_class.id}
        response = {'banner': banner}
        return JsonResponse(response)


class BannerDeleteAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.delete_banner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        Banner.objects.get(id=banner_id).delete()
        response = {'deleted': True}
        return JsonResponse(response)


class BannerSetAsBaseAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.add_basebanner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        banner = Banner.objects.get(id=banner_id)
        image = Image.open(banner.image.path).convert('RGB')
        descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
        BaseBanner.objects.create(
            author=request.user,
            image=banner.image.name,
            descriptor=descriptor,
            banner_type_id=banner.banner_class_id,
        )
        response = {'created': True}
        return JsonResponse(response)
