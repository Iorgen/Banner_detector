from django.shortcuts import render
from ..models import BannerType
from django.views.generic import TemplateView, View, ListView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
def home(request):
    context = {
        'title': 'Banner_detector',
    }
    return render(request, 'banner_detector/home.html', context)


class BannerTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    template_name = 'banner_type_list.html'
    model = BannerType
    permission_required = 'banner_detector.view_bannertype'
    ordering = ['name']
    context_object_name = 'banner_types'
    paginate_by = 15


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
