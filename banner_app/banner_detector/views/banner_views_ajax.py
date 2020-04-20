from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import Banner, BannerType, BaseBanner
from django.views.generic import (View)
from django.conf import settings


class BannerUpdateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """ Update banner type for income banner
    Create base_banner using banner_object from banner
    Recalculate distance between banner and new base_banner
    """
    permission_required = 'banner_detector.change_banner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        banner_type_id = request.GET.get('bannerTypeId', None)
        banner = Banner.objects.get(id=banner_id)
        banner_type = BannerType.objects.filter(pk=banner_type_id).first()
        with transaction.atomic():
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
    """ Delete banner instance by banner id
    """
    permission_required = 'banner_detector.delete_banner'

    def get(self, request):
        banner_id = request.GET.get('id', None)
        Banner.objects.get(id=banner_id).delete()
        response = {'deleted': True}
        return JsonResponse(response)


class BannerSetAsBaseAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """ Create new base_banner instance based on banner. Set base banner for incoming banner.
    """
    permission_required = 'banner_detector.add_basebanner'

    def get(self, request):
        with transaction.atomic():
            banner_id = request.GET.get('id', None)
            # banner_type_id = request.GET.get('banner_type_id', None)
            banner = Banner.objects.get(id=banner_id)
            base_banner, base_banner_created = BaseBanner.objects.get_or_create(
                banner_object_id=banner.banner_object.id,
                author=request.user,
            )
            banner.base_banner = base_banner
            banner.save()
            response = {'base_banner_created': base_banner_created}
        return JsonResponse(response)


class BannerSetAsGarbageAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Get banner by id from DB
    Get banner_type by default trash name
    Set banner.banner_type = banner_type
    Create base banner with update banner object
    Set base banner for banner
    Save banner (override distance)
    """
    permission_required = 'banner_detector.add_basebanner'

    def post(self, request):
        with transaction.atomic():
            banner_id = request.POST.get('id', None)
            try:
                banner = Banner.objects.get(pk=banner_id)
                banner_type = BannerType.objects.filter(name=settings.GARBAGE_BANNER_TYPE).first()
                banner_object = banner.banner_object
                banner_object.banner_type = banner_type
                banner_object.save()
                # Create base banner
                base_banner = BaseBanner.objects.create(
                    banner_object=banner_object,
                    author=request.user,
                )
                # Set base banner for banner
                banner.base_banner = base_banner
                banner.save()
                response = {'set': True}
                return JsonResponse(response)
            except Exception:
                response = {'set': False}
                return JsonResponse(response)


class BannerSetAsSocialAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Get banner by id from DB
    Get banner_type by default social name
    Set banner.banner_type = banner_type
    Create base banner with update banner object
    Set base banner for banner
    Save banner (override distance)
    """
    permission_required = 'banner_detector.add_basebanner'

    def post(self, request):
        with transaction.atomic():
            banner_id = request.POST.get('id', None)
            try:
                banner = Banner.objects.get(pk=banner_id)
                banner_type = BannerType.objects.filter(name=settings.SOCIAL_BANNER_TYPE).first()
                banner_object = banner.banner_object
                banner_object.banner_type = banner_type
                banner_object.save()
                # Create base banner
                base_banner = BaseBanner.objects.create(
                    banner_object=banner_object,
                    author=request.user,
                )
                # Set base banner for banner
                banner.base_banner = base_banner
                banner.save()
                response = {'set': True}
                return JsonResponse(response)
            except Exception:
                response = {'set': False}
                return JsonResponse(response)
