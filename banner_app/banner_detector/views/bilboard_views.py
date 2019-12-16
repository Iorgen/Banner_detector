import os
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..tasks import recognize_banners
from ..forms import BillboardImageCreationForm
from ..models import Billboard, Banner, BannerObject
from ML_detector.core.controller import ObjectDetectionController, ObjectRecognitionController
from django.template.loader import render_to_string
from django.views.generic import (View, ListView, DetailView, CreateView, DeleteView)
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import ProtectedError


class BillboardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    model = Billboard
    template_name = 'banner_detector/billboard/billboards_list.html'
    permission_required = 'banner_detector.view_billboard'
    context_object_name = 'billboards'
    ordering = ['-date_added']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BillboardListView, self).get_context_data(**kwargs)
        return context


class UserBillboardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    model = Billboard
    template_name = 'banner_detector/billboard/user_billboards_list.html'
    permission_required = 'banner_detector.view_billboard'
    context_object_name = 'billboards'
    ordering = ['-date_added']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return self.model.objects.filter(author=user).order_by('date_added')


class BillboardDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """

    """
    template_name = 'banner_detector/billboard/billboard_detail.html'
    permission_required = 'banner_detector.view_billboard'
    model = Billboard
    context_object_name = 'billboard'

    def get_context_data(self, **kwargs):
        context = super(BillboardDetailView, self).get_context_data(**kwargs)
        banners = Banner.objects.filter(billboard__id=self.object.id)
        context['banners'] = banners
        return context


class BillboardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """

    """
    model = Billboard
    form_class = BillboardImageCreationForm
    permission_required = 'banner_detector.add_billboard'
    template_name = 'banner_detector/billboard/billboard_form.html'

    def get(self, request, *args, **kwargs):
        form = BillboardImageCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            billboard_form = form.save(commit=True)
            billboard = Billboard.objects.get(pk=billboard_form.id)
            banners_crops = ObjectDetectionController().banner_detection(billboard)
            # TODO fix костыль связанный с несовместимостью путей Django и image.ai
            billboard.detected_image.name = os.path.join(
                'detected_banners', billboard.image.name)
            banner_ids = []
            # _banners = []
            for idx, banner_crop in enumerate(banners_crops[1]):
                with transaction.atomic():
                    banner_object = BannerObject()
                    banner_object.image.name = banner_crop[6:]
                    image = ObjectRecognitionController().open_image(banner_object.image.path)
                    banner_object.descriptor = ObjectRecognitionController().get_descriptor(image).tolist()

                    banner_object.save()
                    banner_object = BannerObject.objects.get(id=banner_object.id)
                    banner = Banner()
                    banner.billboard = billboard
                    banner.author = request.user
                    banner.banner_object = banner_object
                    banner.save()
                    banner_ids.append(banner.id)
            recognize_banners.delay(banner_ids)
            # recognize_banners(banner_ids)
            billboard.save()
            messages.add_message(self.request, messages.INFO, 'Биллборд загружен, банеры отправлены на распознавание')
            # if request.user.groups.all()
            # return redirect(reverse('billboard-detail', kwargs={'pk': billboard_form.id}))
            return redirect(reverse('billboard-create'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Заполните все поля формы')
            return render(request, self.template_name, {'form': form})


class BillboardDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Billboard
    template_name = "banner_detector/billboard/billboard_confirm_delete.html"
    success_url = '/'
    context_object_name = 'billboard'
    permission_required = 'banner_detector.delete_billboard'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'Can not delete: this parent has a child!')
            return  # The url of the delete view (or whatever you want)

        messages.add_message(request, messages.ERROR, 'Биллборд успешно удалён')
        return HttpResponseRedirect(success_url)


class BillboardXmlExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    template_name = 'banner_detector/billboard/billboard_detail.html'
    permission_required = 'banner_detector.view_billboard'
    model = Billboard
    context_object_name = 'billboard'

    def get(self, request, id):
        billboard = Billboard.objects.get(id=id)
        banners = Banner.objects.filter(billboard_id=billboard.pk, banner_object__banner_type__isnull=False)
        xml = render_to_string('banner_detector/banner_info.xml',
                               {'banners': banners, 'billboard': billboard})
        return HttpResponse(xml)
