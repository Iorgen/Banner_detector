from django.shortcuts import render
from ..models import Bus
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
def home(request):
    context = {
        'title': 'Banner_detector',
    }
    return render(request, 'banner_detector/home.html', context)


class BusListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    template_name = 'bus_list.html'
    model = Bus
    permission_required = 'banner_detector.view_bus'
    ordering = ['bus_number']
    context_object_name = 'buses'
    paginate_by = 15


class BusCreateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.add_bus'

    def get(self, request):
        number = request.GET.get('number', None)
        bus_object = Bus.objects.create(
            bus_number=number
        )
        bus = {'id': bus_object.id,
               'number': bus_object.bus_number}

        response = {
            'bus': bus
        }
        return JsonResponse(response)


class BusDeleteAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.delete_bus'

    def get(self, request):
        bus_id = request.GET.get('id', None)
        Bus.objects.get(id=bus_id).delete()
        response = {
            'deleted': True
        }
        return JsonResponse(response)


class BusUpdateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.change_bus'

    def get(self, request):
        bus_id = request.GET.get('id', None)
        number = request.GET.get('number', None)

        bus_object = Bus.objects.get(id=bus_id)
        bus_object.bus_number = number
        bus_object.save()

        bus = {'id': bus_object.id,
               'number': bus_object.bus_number}

        response = {
            'bus': bus
        }
        return JsonResponse(response)
