from django.contrib import admin
from .models import Bus, Billboard, Banner, BaseBanner, BannerType, BannerObject, BillboardType


admin.site.register(Bus)
admin.site.register(Billboard)
admin.site.register(Banner)
admin.site.register(BannerType)
admin.site.register(BaseBanner)
admin.site.register(BannerObject)
admin.site.register(BillboardType)
