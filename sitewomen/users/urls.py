from django.urls import path, re_path, register_converter
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="login"), # 'users:login'
    path('logout/', LogoutView.as_view(), name="logout"), # 'users.logout'
    
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    # в базовый класс представления можно передавать атрибуты и extra_context
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]


