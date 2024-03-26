from django.urls import path, re_path, register_converter
from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name="login"), # 'users:login'
    path('logout/', views.logout_user, name="logout"), # 'users.logout'
]


