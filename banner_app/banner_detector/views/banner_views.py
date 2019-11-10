from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from ..models import Banner, BannerType
from django.views.generic import (View, ListView, DetailView)


class BannerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    model = Banner
    template_name = 'banner_detector/banner/banner_list.html'
    permission_required = 'banner_detector.view_banner'
    ordering = ['billboard']
    context_object_name = 'banners'
    paginate_by = 15
    list_header = 'Все баннеры'

    def get_context_data(self, **kwargs):
        context = super(BannerListView, self).get_context_data(**kwargs)
        context['list_header'] = self.list_header
        context['banner_types'] = BannerType.objects.all()
        return context


class UserBannerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    model = Banner
    template_name = 'banner_detector/banner/banner_list.html'
    permission_required = 'banner_detector.view_banner'
    context_object_name = 'banners'
    paginate_by = 15
    list_header = 'Список баннеров от'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return self.model.objects.filter(billboard__author=user).order_by('pk')

    def get_context_data(self, **kwargs):
        context = super(UserBannerListView, self).get_context_data(**kwargs)
        context['list_header'] = self.list_header
        context['banner_types'] = BannerType.objects.all()
        return context


class UnknownBannerListView(LoginRequiredMixin, ListView):
    """

    """
    model = Banner
    template_name = 'banner_detector/banner/banner_list.html'
    permission_required = 'banner_detector.view_banner'
    context_object_name = 'banners'
    paginate_by = 15
    list_header = 'Список баннеров с неизвестным классом'

    def get_queryset(self):
        return Banner.get_unknown_banners()

    def get_context_data(self, **kwargs):
        context = super(UnknownBannerListView, self).get_context_data(**kwargs)
        context['list_header'] = self.list_header
        context['banner_types'] = BannerType.objects.all()
        return context


class BannerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """

    """
    template_name = 'banner_detector/banner/banner_detail.html'
    model = Banner
    context_object_name = 'banner'
    permission_required = 'banner_detector.view_banner'

    def get_context_data(self, **kwargs):
        context = super(BannerDetailView, self).get_context_data(**kwargs)
        return context
