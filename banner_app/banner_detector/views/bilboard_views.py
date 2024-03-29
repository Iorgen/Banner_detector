import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import (View, ListView, DetailView, CreateView, DeleteView)
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import ProtectedError
from django.http import JsonResponse
from datetime import date, datetime
from django.conf import settings
from ..tasks import recognize_banners, recognize_billboards_from_rar
from ..forms import BillboardImageCreationForm, ImportBillboardsForm, XMLExportForm
from ..models import Billboard, Banner, BannerObject, Bus, BannerType
from ML_detector.core.controller import ObjectDetectionController, ObjectRecognitionController


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
        context['garbage_banner_type_name'] = settings.GARBAGE_BANNER_TYPE
        context['social_banner_type_name'] = settings.SOCIAL_BANNER_TYPE
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
        context['active_banner_types'] = BannerType.objects.filter(active=True)
        context['in_active_banner_types'] = BannerType.objects.filter(active=False)
        context['garbage_banner_type_name'] = settings.GARBAGE_BANNER_TYPE
        context['social_banner_type_name'] = settings.SOCIAL_BANNER_TYPE
        return context


class BillboardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # TODO create normal ajax view
    """ Ajax view for added new stand in the system and then send to recognizer

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
            billboard.detected_image.name = os.path.join('detected_banners', billboard.image.name)
            banner_ids = []
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
            # recognize_banners.apply_async(args=[banner_ids])
            recognize_banners.delay(banner_ids=banner_ids)
            billboard.save()
            response = {'recognize': True}
            return JsonResponse(response)
        else:
            response = {'recognize': False}
            return JsonResponse(response)


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
    """ Return download link for xml with passed stand id

    """
    template_name = 'banner_detector/banner_info.xml'
    permission_required = 'banner_detector.view_billboard'
    model = Billboard
    context_object_name = 'billboard'

    def get(self, request, id):
        billboard = Billboard.objects.get(id=id)
        banners = Banner.objects.filter(billboard_id=billboard.pk, banner_object__banner_type__isnull=False)
        xml = render_to_string(self.template_name,
                               {'banners': banners, 'billboard': billboard})
        response = HttpResponse(xml)
        response['Content-Disposition'] = 'attachment; filename="' + str(billboard.date_added) + '.xml"'
        return response


class TodayBillboardsXmlExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """ Return download link for xml with today stands

    """
    template_name = 'banner_detector/today_banner_info.xml'
    permission_required = 'banner_detector.view_billboard'
    model = Billboard
    context_object_name = 'billboard'

    def get(self, request):
        today = date.today()
        today_buses = Billboard.objects.filter(date_added__year=today.year,
                                               date_added__month=today.month,
                                               date_added__day=today.day).values_list('bus_id').distinct()
        # TODO check how i can
        today_buses = Bus.objects.filter(id__in=today_buses)
        xml = render_to_string(self.template_name, {
            'buses': today_buses,
            'today': date.today()
        })
        response = HttpResponse(xml)
        response['Content-Disposition'] = 'attachment; filename="' + str(today) + '.xml"'
        return response


class ImportBillboards(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    form_class = ImportBillboardsForm
    permission_required = 'banner_detector.add_basebanner'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'banner_detector/import_billboards.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            default_storage.save('temporary_files/billboards/recognize.zip',
                                 ContentFile(request.FILES['archive_file'].read()))
            recognize_billboards_from_rar.delay('temporary_files/billboards/recognize.zip', request.user.id)
            messages.add_message(self.request, messages.INFO, 'стенды загружены и отправлены на распознавание')
            return redirect(reverse('detector-home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, 'banner_detector/import_base_banners.html', {'form': form})


class XmlExportPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    template_name = 'banner_detector/interval_banner_info.xml'
    permission_required = 'banner_detector.view_billboard'
    form_class = XMLExportForm
    model = Billboard

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'banner_detector/export_templates/XML_export.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Get date from POST form
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            # Convert to datetime and set hour and minute
            datetime_from = datetime(year=date_from.year, month=date_from.month, day=date_from.day, hour=0, minute=0)
            datetime_to = datetime(year=date_to.year, month=date_to.month, day=date_to.day, hour=23, minute=59)
            # Get interval buses
            current_buses = Billboard.objects.filter(
                date_added__lte=datetime_to,
                date_added__gte=datetime_from,

            ).values_list('bus_id').distinct()
            # TODO check how i can
            current_buses = Bus.objects.filter(id__in=current_buses)
            bus_billboards_list = []
            for bus in current_buses:
                bus_billboards_list.extend(bus.interval_billboards(datetime_from, datetime_to))

            xml = render_to_string(self.template_name, {
                'datetime_from': datetime_from,
                'datetime_to': datetime_to,
                'buses': current_buses,
                'billboards_list': bus_billboards_list
            })
            response = HttpResponse(xml)
            response['Content-Disposition'] = 'attachment; filename="' + str(datetime_from) + str(datetime_to) + '.xml"'
            return response
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, 'banner_detector/export_templates/XML_export.html', {'form': form})
