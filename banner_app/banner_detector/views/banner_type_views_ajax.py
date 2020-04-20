from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from ..models import BannerType
from ..forms import BannerTypeCreationForm
from django.views.generic import View, CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from PIL import Image


# Create your views here.
def home(request):
    context = {
        'title': 'Banner_detector',
    }
    return render(request, 'banner_detector/home.html', context)


class BannerTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View for new banner type creation
    """
    model = BannerType
    form_class = BannerTypeCreationForm
    template_name = 'banner_detector/banner_type_list.html'
    permission_required = 'banner_detector.add_bannertype'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                form.instance.author = request.user
                banner_type_object = form.save(commit=True)
                messages.add_message(self.request, messages.INFO, f'Тип баннера {banner_type_object.name} загружен и добавлен')
            return redirect(reverse('detector-home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, self.template_name, {'form': form})


class BannerTypeCreateAJAXView(LoginRequiredMixin, View):

    def get(self, request):
        name = request.GET.get('name', None)
        banner_type_object = BannerType.objects.create(
            name=name,
            author=request.user
        )
        banner_type = {
            'id': banner_type_object.id,
            'name': banner_type_object.name
        }
        response = {
            'banner_type': banner_type
        }
        return JsonResponse(response)


class BannerTypeUpdateAJAXView(View):

    def get(self, request):
        banner_type_id = request.GET.get('id', None)
        name = request.GET.get('name', None)

        banner_type_object = BannerType.objects.get(id=banner_type_id)
        banner_type_object.name = name
        banner_type_object.save()

        banner_type = {'id': banner_type_object.id,
                       'name': banner_type_object.name}
        response = {
            'banner_type': banner_type
        }
        return JsonResponse(response)
