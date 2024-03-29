from django.urls import path
from .views.views import (home, ImportBaseBanners, ImportBannersTypesFromFile)
from .views.task_views import (ImportBannersTypesFromUrl, UpdateBannerObjectsDescriptors)

from .views.bus_views import (BusCreateAJAXView, BusDeleteAJAXView, BusListView, BusUpdateAJAXView)
from .views.bilboard_views import (BillboardListView, UserBillboardListView,
                                   BillboardDetailView, BillboardCreateView, BillboardXmlExportView,
                                   BillboardDeleteView, TodayBillboardsXmlExportView, ImportBillboards, XmlExportPage)
from .views.base_banner_views import (BaseBannerCreateView, BaseBannerDetailView,
                                      BaseBannerListView, BaseBannerDeleteView)
from .views.banner_views import (BannerListView, UserBannerListView, UnknownBannerListView,
                                 BannerDetailView)
from .views.banner_views_ajax import (BannerUpdateAJAXView, BannerDeleteAJAXView,
                                      BannerSetAsBaseAJAXView, BannerSetAsGarbageAJAXView,
                                      BannerSetAsSocialAJAXView
                                      )
from .views.banner_type_views_ajax import (BannerTypeCreateAJAXView, BannerTypeCreateView, BannerTypeUpdateAJAXView)
from .views.stand_type_views import (StandTypeCreateView)


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
    path('billboard/today_xml/', TodayBillboardsXmlExportView.as_view(), name='today-billboard-xml-detail'),
    path('billboard/xml_interval/', XmlExportPage.as_view(), name='interval-billboard-xml-detail'),

    path('billboard/<int:pk>/delete/', BillboardDeleteView.as_view(), name='billboard-delete'),

    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='billboard-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='billboard-delete'),

    # Base Banners class views
    path('base_banners/', BaseBannerListView.as_view(), name='base-banners'),
    path('base_banners/create/', BaseBannerCreateView.as_view(), name='base-banner-create'),
    path('base_banners/<int:pk>/', BaseBannerDetailView.as_view(), name='base-banner-detail'),
    # path('base_banners/<int:pk>/update/', BaseBannerUpdateView.as_view(), name='base-banner-update'),
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
    path('banners/crud/set-as-garbage/', BannerSetAsGarbageAJAXView.as_view(), name='banner-ajax-set-as-garbage'),
    path('banners/crud/set-as-social/', BannerSetAsSocialAJAXView.as_view(), name='banner-ajax-set-as-social'),

    # Bus Ajax CRUD Operations
    path('buses/', BusListView.as_view(), name='buses'),
    path('buses/crud/add/', BusCreateAJAXView.as_view(), name='bus-ajax-add'),
    path('buses/crud/update/', BusUpdateAJAXView.as_view(), name='bus-ajax-update'),
    path('buses/crud/delete/', BusDeleteAJAXView.as_view(), name='bus-ajax-delete'),

    # BannerTypes Pages
    path('banner_type/', BannerTypeCreateView.as_view(), name='create-banner-type'),
    # BannerType Ajax CRUD Operations

    path('banner_type/crud/add/', BannerTypeCreateAJAXView.as_view(), name='banner-type-ajax-add'),
    path('banner_type/crud/update/', BannerTypeUpdateAJAXView.as_view(), name='banner-type-ajax-update'),
    # path('banner_type/crud/delete/', BusDeleteAJAXView.as_view(), name='banner-type-ajax-delete'),

    # Stand type views
    path('stand_type/create', StandTypeCreateView.as_view(), name='create-stand-type'),

    # Import Base Banner
    path('import_base_banners/', ImportBaseBanners.as_view(), name='import-base-banners'),
    # Import banner types
    path('import_banners_type/', ImportBannersTypesFromFile.as_view(), name='import-banners-type'),
    # Import billboards
    path('import_billboards/', ImportBillboards.as_view(), name='import-billboards'),

    # Task views
    path('import_banners_type_from_url/', ImportBannersTypesFromUrl.as_view(), name='task-import-banners-type-url'),
    path('update_banner_objects_descriptors/', UpdateBannerObjectsDescriptors.as_view(), name='task-update-banner-objects')


]
