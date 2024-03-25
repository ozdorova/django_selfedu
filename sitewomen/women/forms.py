from turtle import title
from typing import Any
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.forms import ValidationError, widgets
from django.utils.deconstruct import deconstructible
from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    # Валидатор. проверяет что в поле присутствуют только русские символы
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None) -> None:
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел'

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise forms.ValidationError(self.message, code=self.code)



# форма связанная с моделью
class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория', 
        empty_label='Не выбрано',
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False, 
        label='Муж', 
        empty_label='Не замужен'
    )
    
    class Meta:
        model = Women
        fields = [
            'title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags'
        ]
        #'__all__' # отображение полей БД, кроме автоматических
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels ={
            'slug': 'URL'
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длинна превышает 50 символов')
        
        return title
    
# форма для загрузки файлов
class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')
    