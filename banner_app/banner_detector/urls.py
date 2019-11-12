from django.urls import path
from .views.views import home
from .views.views import (BusCreateAJAXView, BusDeleteAJAXView, BusListView, BusUpdateAJAXView)
from .views.bilboard_views import (BillboardListView, UserBillboardListView,
                                   BillboardDetailView, BillboardCreateView, BillboardXmlExportView)
from .views.base_banner_views import (BaseBannerCreateView, BaseBannerDetailView,
                                      BaseBannerListView, BaseBannerUpdateView, BaseBannerDeleteView)
from .views.banner_views import (BannerListView, UserBannerListView, UnknownBannerListView,
                                 BannerDetailView)
from .views.banner_views_ajax import (BannerUpdateAJAXView, BannerDeleteAJAXView, BannerSetAsBaseAJAXView)
from .views.banner_type_views_ajax import (BannerTypeCreateAJAXView, BannerTypeListView, BannerTypeUpdateAJAXView)

urlpatterns = [
    # Main app page
    path('', home, name='detector-home'),

    # Billboard views
    path('billboards/', BillboardListView.as_view(), name='billboards'),
    path('billboards/<str:username>', UserBillboardListView.as_view(), name='user-billboards'),
    path('billboards/<int:pk>/', BillboardDetailView.as_view(), name='billboard-detail'),
    path('billboards/new/', BillboardCreateView.as_view(), name='billboard-create'),
    # XML Export view
    path('billboard/xml/<int:id>', BillboardXmlExportView.as_view(), name='billboard-xml-detail'),

    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='billboard-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='billboard-delete'),

    # Base Banners class views
    path('base_banners/', BaseBannerListView.as_view(), name='base-banners'),
    path('base_banners/create/', BaseBannerCreateView.as_view(), name='base-banner-create'),
    path('base_banners/<int:pk>/', BaseBannerDetailView.as_view(), name='base-banner-detail'),
    path('base_banners/<int:pk>/update/', BaseBannerUpdateView.as_view(), name='base-banner-update'),
    path('base_banners/<int:pk>/delete/', BaseBannerDeleteView.as_view(), name='base-banner-delete'),

    # Banner views
    path('banners/', BannerListView.as_view(), name='banners'),
    path('banners/<int:pk>', BannerDetailView.as_view(), name='banner-detail'),
    path('banners/<str:username>', UserBannerListView.as_view(), name='user-banners'),
    path('banners/non_recognized/', UnknownBannerListView.as_view(), name='non-recognized-banners'),

    # Banner Ajax CRUD Operations
    path('banners/crud/delete/', BannerDeleteAJAXView.as_view(), name='banner-ajax-delete'),
    path('banners/crud/update/', BannerUpdateAJAXView.as_view(), name='banner-ajax-update'),
    path('banners/crud/set-as-base/', BannerSetAsBaseAJAXView.as_view(), name='banner-ajax-set-as-base'),

    # Bus Ajax CRUD Operations
    path('buses/', BusListView.as_view(), name='buses'),
    path('buses/crud/add/', BusCreateAJAXView.as_view(), name='bus-ajax-add'),
    path('buses/crud/update/', BusUpdateAJAXView.as_view(), name='bus-ajax-update'),
    path('buses/crud/delete/', BusDeleteAJAXView.as_view(), name='bus-ajax-delete'),

    # Bus Ajax CRUD Operations
    path('banner_type/', BannerTypeListView.as_view(), name='banner-types'),
    path('banner_type/crud/add/', BannerTypeCreateAJAXView.as_view(), name='banner-type-ajax-add'),
    path('banner_type/crud/update/', BannerTypeUpdateAJAXView.as_view(), name='banner-type-ajax-update'),
    # path('banner_type/crud/delete/', BusDeleteAJAXView.as_view(), name='banner-type-ajax-delete'),

]
