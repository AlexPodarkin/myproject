from django import forms
from django.core.exceptions import ValidationError
from . import models


class AddOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_sign'].empty_label = 'эскиз не выбран'
        self.fields['form_sign'].label = 'Форма таблички'
        self.fields['form_sign'].widget.attrs['class'] = 'select1'
        self.fields['color_sign'].label = 'Цвет таблички '
        self.fields['address_sign'].label = 'Адрес (изделия) '
        self.fields['customer_name'].label = 'Имя заказчика'
        self.fields['customer_email'].label = 'Email '
        self.fields['customer_phone'].label = 'Номер телефона '

    class Meta:
        model = models.Order
        fields = ['form_sign', 'color_sign', 'address_sign', 'customer_name', 'customer_email', 'customer_phone']
        choices = (('синий', 'синий'), ('коричневый', 'коричневый'), ('зеленый', 'зеленый'),
                   ('бордовый', 'бордовый'), ('обсудить по телефону', 'обсудить по телефону'),)
        widgets = {
            'color_sign': forms.Select(attrs={'class': 'select2'}, choices=choices),
            'address_sign': forms.TextInput(attrs={'placeholder': '*ул.Братская,д.5', 'class': 'input1'}),
            'customer_name': forms.TextInput(attrs={'placeholder': '*Введите имя', 'class': 'input2'}),
            'customer_email': forms.EmailInput(attrs={'placeholder': '*my@pochta.com', 'class': 'input3'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': '*в любом формате', 'class': 'input4'}),
        }

    # пользовательская валидация
    def clean_customer_name(self):
        customer_name = self.cleaned_data['customer_name']
        if len(customer_name) < 2:
            raise ValidationError('введите корректные данные')
        return customer_name


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_autor'].label = ''
        self.fields['review_autor'].label = ''

    class Meta:
        model = models.Review
        fields = ['name_autor', 'review_autor']
        widgets = {
            'name_autor': forms.TextInput(attrs={'placeholder': '*Введите имя', 'class': 'our_works'}),
            'review_autor': forms.Textarea(attrs={'placeholder': '*Ваш отзыв (не более 100 символов)',
                                                  'class': 'our_works', 'cols': 45, 'rows': 4}),
        }

    # пользовательская валидация
    def clean_name_autor(self):
        customer_name = self.cleaned_data['name_autor']
        if len(customer_name) < 2:
            raise ValidationError('введите корректные данные')
        return customer_name

    def clean_review_autor(self):
        customer_name = self.cleaned_data['review_autor']
        if len(customer_name) < 7:
            raise ValidationError('Не стесняйтесь, пишите больше)')
        return customer_name
