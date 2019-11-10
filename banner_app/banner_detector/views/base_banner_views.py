from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from ML_detector.core.controller import ObjectRecognitionController
from ..forms import BaseBannerCreationForm
from ..models import BaseBanner
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView)
from PIL import Image


class BaseBannerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """

    """
    model = BaseBanner
    form_class = BaseBannerCreationForm
    template_name = 'banner_detector/base_banner/base_banner_form.html'
    permission_required = 'banner_detector.add_basebanner'

    def get(self, request, *args, **kwargs):
        form = BaseBannerCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        # TODO Fill try exceptions
        if form.is_valid():
            form.instance.author = request.user
            image = request.FILES['image']
            image = Image.open(image).convert('RGB')
            form.instance.descriptor = ObjectRecognitionController().get_descriptor(image).tolist()
            banner_form = form.save(commit=True)
            messages.add_message(self.request, messages.INFO, 'Баннер загружен и добавлен в модель анализатора')
            return redirect(reverse('base-banner-detail', kwargs={'pk': banner_form.id}))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, self.template_name, {'form': form})


class BaseBannerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """

    """
    template_name = 'banner_detector/base_banner/base_banner_detail.html'
    model = BaseBanner
    context_object_name = 'banner'
    permission_required = 'banner_detector.view_basebanner'

    def get_context_data(self, **kwargs):
        context = super(BaseBannerDetailView, self).get_context_data(**kwargs)
        return context


class BaseBannerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    template_name = 'banner_detector/base_banner/base_banner_list.html'
    model = BaseBanner
    permission_required = 'banner_detector.view_basebanner'
    ordering = ['date_added']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(BaseBannerListView, self).get_context_data(**kwargs)
        p = Paginator(BaseBanner.objects.select_related().all(), self.paginate_by)
        context['banner_base_images'] = p.page(context['page_obj'].number)
        return context


class BaseBannerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BaseBanner
    template_name = "banner_detector/base_banner/base_banner_form.html"
    permission_required = 'banner_detector.change_basebanner'
    fields = ['banner_type', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        base_banner = self.get_object()
        if self.request.user == base_banner.author:
            return True
        return False


class BaseBannerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BaseBanner
    template_name = "banner_detector/base_banner/base_banner_confirm_delete.html"
    success_url = '/'
    permission_required = 'banner_detector.delete_basebanner'

    def test_func(self):
        base_banner = self.get_object()
        if self.request.user == base_banner.author:
            return True
        return False
