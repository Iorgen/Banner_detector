from django.contrib import admin
from .models import Bus, BillboardImage, Banner, BaseBanner, BannerType


admin.site.register(Bus)
admin.site.register(BillboardImage)
admin.site.register(Banner)
admin.site.register(BannerType)
admin.site.register(BaseBanner)
