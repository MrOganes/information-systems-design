# forms.py
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'city',
            'postal_code',
            'country'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone_number': 'Номер телефона',
            'address': 'Адрес',
            'city': 'Город',
            'postal_code': 'Почтовый индекс',
            'country': 'Страна'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if ' ' in first_name:
            raise ValidationError("Имя пользователя не должно содержать пробелов.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if ' ' in last_name:
            raise ValidationError("Фамилия пользователя не должна содержать пробелов.")
        return last_name

    def clean_phone_number(self):
        phone_regex = r"^\+?[0-9]{10,15}$"
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            return ''
        if phone_number and re.match(phone_regex, phone_number):
            return phone_number
        raise ValueError("Номер телефона должен состоять из 10-15 цифр, по желанию начинатся с +.")

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code:
            try:
                int(postal_code)
            except Exception:
                raise ValueError("Почтовый индекс должен состоять из цифр.")
        else:
            return ""

        if len(str(postal_code)) <= 10:
            return postal_code
        raise ValueError("Почтовый индекс должен содержать до 10 цифр.")
