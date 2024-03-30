from django.urls import path, re_path, register_converter, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


app_name = 'users'

urlpatterns = [
    
    path('login/', views.LoginUser.as_view(), name="login"), # 'users:login'
    path('logout/', LogoutView.as_view(), name="logout"), # 'users.logout'
    
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    # в базовый класс представления можно передавать атрибуты и extra_context
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    # путь если пароль успешно изменен
    path(
        'password-change/done/', 
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
            ), 
        name='password_change_done',
    ),
    ### Восстановление пароля
    # путь на шаблон отправки емейла для восстановление пароля
    path(
        'password-reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            success_url=reverse_lazy('users:password_reset_done'),
        ), 
        name='password_reset',
    ),
    # шаблон с сообщение об успешной отправке информации на емейл
    path(
        'password-reset/done/', 
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ), 
        name='password_reset_done',
    ),
    # путь на шаблон непосредственно для восстановление пароля
    path('password-reset/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete'),
        ), 
        name='password_reset_confirm',
    ),
    # путь на шаблон если пароль был успешно восстановлен
    path(
        'password-reset/complete/', 
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
            ), 
        name='password_reset_complete'
    ),
    
]


