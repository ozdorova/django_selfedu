from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from numpy import extract
from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class RegisterUser(CreateView):
    # класс представление для регистрации
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    # класс предстваление для профиля пользователя
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extract_context = {'title': 'Профиль пользователя'}
    
    def get_success_url(self) -> str:
        # перенаправление после изменения
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        # получаем обьект авторизованного пользователя, чтобы нельзя было менять данные других пользователей
        return self.request.user

class LoginUser(LoginView):
    # класс представления для входа
    form_class = LoginUserForm # AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация'
    }


class UserPasswordChange(PasswordChangeView):
    # класс представление для смены пароля
    form_class = UserPasswordChangeForm
    # перенаправляет на password_change_done.html
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'

    # def get_success_url(self) -> str:
    #     return reverse_lazy('home')
    # либо LOGIN_REDIRECT_URL = 'home' в settings.py

# # функция входа в систему
# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
            
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})


# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login')) # users - пространство имен


#  def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password']) # формирование хеш пароля 
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})
