import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..tasks import recognize_banners
from ..forms import BillboardImageCreationForm
from ..models import BillboardImage, Banner
from ML_detector.core.controller import ObjectDetectionController
from django.template.loader import render_to_string
from django.views.generic import (View, ListView, DetailView, CreateView)
from django.http import HttpResponse


class BillboardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    model = BillboardImage
    template_name = 'banner_detector/billboard/billboards_list.html'
    permission_required = 'banner_detector.view_billboardimage'
    context_object_name = 'billboards'
    ordering = ['date_added']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BillboardListView, self).get_context_data(**kwargs)
        return context


class UserBillboardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    model = BillboardImage
    template_name = 'banner_detector/billboard/user_billboards_list.html'
    permission_required = 'banner_detector.view_billboardimage'
    context_object_name = 'billboards'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return self.model.objects.filter(author=user).order_by('date_added')


class BillboardDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """

    """
    template_name = 'banner_detector/billboard/billboard_detail.html'
    permission_required = 'banner_detector.view_billboardimage'
    model = BillboardImage
    context_object_name = 'billboard'

    def get_context_data(self, **kwargs):
        context = super(BillboardDetailView, self).get_context_data(**kwargs)
        banners = Banner.objects.filter(billboard__id=self.object.id)
        context['banners'] = banners
        return context


class BillboardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """

    """
    model = BillboardImage
    form_class = BillboardImageCreationForm
    permission_required = 'banner_detector.change_billboardimage'
    template_name = 'banner_detector/billboard/billboard_form.html'

    def get(self, request, *args, **kwargs):
        form = BillboardImageCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            billboard_form = form.save(commit=True)
            billboard = BillboardImage.objects.get(pk=billboard_form.id)
            banners_crops = ObjectDetectionController().banner_detection(billboard)
            banner_ids = []
            for idx, banner_crop in enumerate(banners_crops[1]):
                banner = Banner()
                banner.billboard = billboard
                # TODO fix костыль связанный с несовместимостью путей Django и image.ai
                banner.image.name = banner_crop[6:]
                banner.save()
                banner_ids.append(banner.id)
            recognize_banners.delay(banner_ids)
            # recognize_banners(banner_ids)
            billboard.detected_image.name = os.path.join(
                'detected_banners', billboard.image.name)
            billboard.save()
            messages.add_message(self.request, messages.INFO, 'Биллборд загружен, банеры отправлены на распознавание')
            return redirect(reverse('billboard-detail', kwargs={'pk': billboard_form.id}))
        else:
            messages.add_message(self.request, messages.ERROR, 'Заполните все поля формы')
            return render(request, self.template_name, {'form': form})


class BillboardXmlExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    template_name = 'banner_detector/billboard/billboard_detail.html'
    permission_required = 'banner_detector.view_billboardimage'
    model = BillboardImage
    context_object_name = 'billboard'

    def get(self, request, id):
        billboard = BillboardImage.objects.get(id=id)
        banners = Banner.objects.filter(billboard_id=billboard.pk, banner_class__isnull=False)
        xml = render_to_string('banner_detector/banner_info.xml',
                               {'banners': banners, 'billboard': billboard})
        return HttpResponse(xml)
