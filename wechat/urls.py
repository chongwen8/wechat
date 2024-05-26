"""
URL configuration for wechat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django import views
from django.contrib import admin
from django.urls import path
from moments.views import show_user, show_status, submit_post, show_friends, LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='home'),
    path('user', show_user),
    path('status', show_status),
    path('post', submit_post),
    path('friends', show_friends),
    path('exit', LogoutView.as_view(next_page = '/'))
]
