from dataclasses import fields
import email
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets

class LoginUserForm(AuthenticationForm):
    # форма для входа в систему
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    #форма регистрации
    # проверки пароля уже есть в UserCreationForm
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    
    class Meta:
        # получение модели бд пользователя
        model = get_user_model()
        # отображаемые поля 
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
        ]
        # дополнительные наименования полей
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        # стили оформления полей
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def clean(self):
        # проверка почты на уникальность
        cleaned_data = super().clean()
        User = get_user_model()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("Эта почта уже зарегестрированна")
        return cleaned_data
    
    
class ProfileUserForm(forms.ModelForm):
    # форма для отображение профиля profile.html
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    email = forms.CharField(
        disabled=True,
        label='E-mail',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'first_name', 'last_name',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    
# class RegisterUserForm(forms.ModelForm)
#     # def clead_email(self):
    #     email = self.cleaned_data['email']
    #     if get_user_model().objects.filter(email=email).exists(): # Это модель из БД
    #         raise forms.ValidationError('Такой E-mail уже существует!')
    #     return email
    
    
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Пароли не совпадают!')
    #     return cd['password']
