from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from ..models import BillboardType
from ..forms import BillboardTypeCreationForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from PIL import Image


class StandTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Create new banner type using ['name', 'image', 'active']
    """
    model = BillboardType
    form_class = BillboardTypeCreationForm
    template_name = 'banner_detector/stand_type/stand_type_create.html'
    permission_required = 'banner_detector.add_billboard'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                form.instance.author = request.user
                stand_type = form.save(commit=True)
                messages.add_message(self.request, messages.INFO, f'Тип стенда {stand_type.name} загружен и добавлен')
            return redirect(reverse('detector-home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка!')
            return render(request, self.template_name, {'form': form})
