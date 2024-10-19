from django import forms
from django.forms import ModelForm

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']

    stop_list = ['казино', 'криптовалюта', 'крипта', 'биржа',
                 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        for stop in self.stop_list:
            if stop in cleaned_data:
                raise forms.ValidationError('Вы пытались создать запрещенный продукт')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        for stop in self.stop_list:
            if stop in cleaned_data:
                raise forms.ValidationError('Вы пытались создать запрещенный продукт')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        exclude = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')  # Получаем продукты из данных
        is_current = cleaned_data.get('is_current')  # Получаем статус активного

        if product and is_current:  # Проверьте, установлен ли продукт и активна ли эта версия
            # Проверьте наличие других активных версий
            active_versions = Version.objects.filter(product=product, is_current=True).exclude(pk=self.instance.pk)
            if active_versions.exists():
                raise forms.ValidationError(
                    'Ошибка: Для этого продукта уже существует активная версия. Пожалуйста, выберите только одну активную версию.')

        return cleaned_data


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ('is_active', 'description', 'category')

