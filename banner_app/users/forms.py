from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # labels = {'username': 'Никнейм', 'password1': 'Пароль',
        #           'password2': 'Подтверждение пароля'}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        # labels = {'username': 'Никнейм', 'email': 'Емэйл'}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'second_name', 'image']
        # labels = {'image': 'Аватар', 'first_name': 'Имя',
        #           'second_name': 'Фамилия'}
