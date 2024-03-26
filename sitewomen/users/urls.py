from django.urls import path, re_path, register_converter
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="login"), # 'users:login'
    path('logout/', LogoutView.as_view(), name="logout"), # 'users.logout'
    path('register/', views.register, name='register'),
]


