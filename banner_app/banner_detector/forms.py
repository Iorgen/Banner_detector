from django import forms
from .models import BillboardImage, BaseBanner, Banner, BannerType, Bus


class BillboardImageCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BillboardImageCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BillboardImage
        fields = ['bus', 'image']
        labels = {'bus': 'Выберите Автобус'}
        widgets = {'image': forms.FileInput(attrs={'id': 'id_image',
                                                   'class': 'inputfile inputfile-1',
                                                   'name': 'file-1[]',
                                                   'data-multiple-caption': '{count} файлов выбрано'
                                                   }),
                   'bus': forms.Select(attrs={'id': 'id_bus',
                                              'class': 'form-control'
                                              })}


class BaseBannerCreationForm(forms.ModelForm):

    class Meta:
        model = BaseBanner
        fields = ['image', 'banner_type']
        labels = {'image': 'Изображение', 'banner_type': 'Класс баннера'}


class BannerTypeCreationForm(forms.ModelForm):

    class Meta:
        model = BannerType
        fields = ['name']
        labels = {'name': 'Название'}


class BannerForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['banner_class', 'id']
        labels = {'banner_class': 'Укажите класс баннера', 'id': 'идентификатор'}


class BusCreationForm(forms.ModelForm):

    class Meta:
        model = Bus
        fields = ['bus_number']
        labels = {'bus_number': 'Номер автобуса'}


class ImportBaseBannersForm(forms.Form):
    archive_file = forms.FileField(widget=forms.FileInput(attrs={'accept':'.zip'}))
