from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import Banner, BannerType, BaseBanner
from django.views.generic import (View)


class BannerUpdateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.change_banner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        banner_type_id = request.GET.get('bannerTypeId', None)
        banner = Banner.objects.get(id=banner_id)
        banner_type = BannerType.objects.filter(pk=banner_type_id).first()
        if banner_type is not None:
            # create base banner instance
            base_banner, banner_created = BaseBanner.objects.get_or_create(
                banner_object=banner.banner_object,
                author=request.user,
            )
            banner.banner_object.banner_type = banner_type
            banner.banner_object.save()
            banner.base_banner = base_banner
            banner.recognition_status = True
            banner.save()
            banner = {'id': banner.id, 'banner_type': banner.banner_object.banner_type.id}
            response = {'banner': banner}
            return JsonResponse(response)
        else:
            response = HttpResponseBadRequest('Wrong banner identifier')
            return response


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
        with transaction.atomic():
            banner_id = request.GET.get('id', None)
            banner_type_id = request.GET.get('banner_type_id', None)
            banner = Banner.objects.get(id=banner_id)
            # banner_type = BannerType.objects.get(pk=banner_type_id)
            base_banner, base_banner_created = BaseBanner.objects.get_or_create(
                banner_object_id=banner.banner_object.id,
                author=request.user,
            )

            response = {'base_banner_created': base_banner_created}
        return JsonResponse(response)
