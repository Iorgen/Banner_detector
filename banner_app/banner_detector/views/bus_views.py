from ..models import Bus, BillboardType
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BusListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """

    """
    template_name = 'bus_list.html'
    model = Bus
    permission_required = 'banner_detector.view_bus'
    # ordering = ['registration_number']
    context_object_name = 'buses'
    # paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(BusListView, self).get_context_data(**kwargs)
        stand_types = BillboardType.objects.all()
        context['stand_types'] = stand_types
        return context


class BusCreateAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.add_bus'

    def get(self, request):
        number = request.GET.get('number', None)
        registration_number = request.GET.get('registrationNumber', None)
        stand_type_id = request.GET.get('standTypeId', None)

        bus_object = Bus.objects.create(
            stand_id=stand_type_id,
            number=number,
            registration_number=registration_number
        )
        print(bus_object.stand)
        bus = {
            'id': bus_object.id,
            'number': bus_object.number,
            'stand': {
                'stand_id': bus_object.stand_id,
                'stand_name': bus_object.stand.name
            },
            'registration_number': bus_object.registration_number
        }

        response = {'bus': bus}
        return JsonResponse(response)


class BusDeleteAJAXView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """

    """
    permission_required = 'banner_detector.delete_bus'

    def get(self, request):
        bus_id = request.GET.get('busId', None)
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
        bus_id = request.GET.get('busId', None)
        standTypeId = request.GET.get('standTypeId', None)
        number = request.GET.get('busNumber', None)
        registration_number = request.GET.get('busRegistrationNumber', None)

        bus_object = Bus.objects.get(id=bus_id)
        bus_object.number = number
        bus_object.stand_id = standTypeId
        bus_object.registration_number = registration_number
        bus_object.save()

        bus = {'id': bus_object.id,
               'number': bus_object.number,
               'registration_number': bus_object.registration_number}

        response = {
            'bus': bus
        }
        return JsonResponse(response)
