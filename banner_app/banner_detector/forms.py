from django import forms
from .models import BillboardImage, BaseBanner, Banner, BannerType, Bus


class BillboardImageCreationForm(forms.ModelForm):

    class Meta:
        model = BillboardImage
        fields = ['bus', 'image']


class BaseBannerCreationForm(forms.ModelForm):

    class Meta:
        model = BaseBanner
        fields = ['image', 'banner_type']


class BannerTypeCreationForm(forms.ModelForm):

    class Meta:
        model = BannerType
        fields = ['name']


class BannerForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['banner_class', 'id']


class BusCreationForm(forms.ModelForm):

    class Meta:
        model = Bus
        fields = ['bus_number']
