from django import forms
from .models import Billboard, BannerObject, Banner, BannerType, Bus, BillboardType
from datetime import date


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
        fields = ['name', 'image', 'active']
        labels = {'name': 'Название', 'image': 'Изображение'}


class BillboardTypeCreationForm(forms.ModelForm):

    class Meta:
        model = BillboardType
        fields = ['serial_number', 'name', 'description']
        labels = {'serial_number': 'Номер', 'name': 'Название', 'description': "Описание"}


class BusCreationForm(forms.ModelForm):

    class Meta:
        model = Bus
        fields = ['registration_number', 'number', 'stand']
        labels = {'registration_number': 'Гос номер автобуса',
                  'number': 'Номер автобуса', 'stand': 'Тип стенда'}


class ImportBaseBannersForm(forms.Form):
    archive_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.zip'}))


class ImportBillboardsForm(forms.Form):
    archive_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.zip'}))


class ImportBannersTypesForm(forms.Form):
    archive_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.tar'}))


class XMLExportForm(forms.Form):
    date_from = forms.DateField(initial=date.today)
    date_to = forms.DateField(initial=date.today)
