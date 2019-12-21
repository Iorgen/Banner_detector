from django.views.generic import View
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..tasks import update_active_banner_types, recalculate_base_banners_descriptors


class ImportBannersTypesFromUrl(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.add_bannertype'

    def get(self, request, *args, **kwargs):
        update_active_banner_types.delay()
        messages.add_message(self.request, messages.INFO, 'Обновление типов баннеров поставлено в очередь')
        return redirect(reverse('detector-home'))


class UpdateBannerObjectsDescriptors(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.add_bannertype'

    def get(self, request, *args, **kwargs):
        recalculate_base_banners_descriptors.delay()
        messages.add_message(self.request, messages.INFO, 'Пересчёт дескрипторов начат ')
        return redirect(reverse('detector-home'))
