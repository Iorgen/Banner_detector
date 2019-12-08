from django import forms
from .models import Billboard, BannerObject, Banner, BannerType, Bus


class BillboardImageCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BillboardImageCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Billboard
        fields = ['bus', 'image']
        labels = {'bus': 'Выберите Автобус'}
        widgets = {'image': forms.FileInput(attrs={'id': 'id_image',
                                                   'class': 'inputfile inputfile-1',
                                                   'name': 'file-1[]',
                                                   'data-multiple-caption': '{count} файлов выбрано',
                                                   'capture': '',
                                                   }),
                   'bus': forms.Select(attrs={'id': 'id_bus',
                                              'class': 'form-control'
                                              })}


class BannerObjectForm(forms.ModelForm):

    class Meta:
        model = BannerObject
        fields = ['image', 'banner_type']
        labels = {'image': 'Изображение', 'banner_type': 'Класс баннера'}


class BannerTypeCreationForm(forms.ModelForm):

    class Meta:
        model = BannerType
        fields = ['name']
        labels = {'name': 'Название'}


class BusCreationForm(forms.ModelForm):

    class Meta:
        model = Bus
        fields = ['registration_number', 'number']
        labels = {'registration_number': 'Гос номер автобуса',
                  'number': 'Номер автобуса'}


class ImportBaseBannersForm(forms.Form):
    archive_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.zip'}))
