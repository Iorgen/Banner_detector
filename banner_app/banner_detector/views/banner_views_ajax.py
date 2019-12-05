from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import Banner, BannerType, BaseBanner
from django.views.generic import (View)
from ML_detector.core.controller import ObjectRecognitionController
from PIL import Image


# class BannerCreateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     """
#
#     """
#     permission_required = 'banner_detector.change_banner'
#
#     def post(self, request):
#         name1 = request.GET.get('name', None)
#         address1 = request.GET.get('address', None)
#         age1 = request.GET.get('age', None)
#
#         obj = Banner.objects.create(
#             name=name1,
#             address=address1,
#             age=age1
#         )
#
#         user = {'id': obj.id, 'name': obj.name,
#                 'address': obj.address, 'age': obj.age}
#
#         data = {
#             'user': user
#         }
#         return JsonResponse(data)


class BannerUpdateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.change_banner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        banner_type_name = request.GET.get('banner_type_name', None)
        banner = Banner.objects.get(id=banner_id)
        banner_type, created = BannerType.objects.get_or_create(
            name=banner_type_name,
            defaults={'author': request.user})
        banner.banner_object.banner_type = banner_type
        banner.banner_object.save()
        banner.recognition_status = True
        banner.save()
        # create base banner instance
        BaseBanner.objects.create(
            banner_object=banner.banner_object,
            author=request.user,
        )
        banner = {'id': banner.id, 'banner_type': banner.banner_object.banner_type.id}
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
        BaseBanner.objects.create(
            banner_object=banner.banner_object,
            author=request.user,

        )
        response = {'created': True}
        return JsonResponse(response)
