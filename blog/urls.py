"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', all_post, name='all_post_url'),
    path('post/create/', PostCreate.as_view(), name='create_post_url'),
    path('post/<str:slug>', PostDetail.as_view(), name='detail_post_url'),
    path('post/<str:slug>/edit/', PostEdit.as_view(), name='edit_post_url'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='delete_post_url'),
    path('tag/', all_tag, name='all_tag_url'),
    path('tag/create/', TagCreate.as_view(), name='create_tag_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='detail_tag_url'),
    path('tag/<str:slug>/edit/', TagEdit.as_view(), name='edit_tag_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='delete_tag_url'),
    path('admin/', admin.site.urls),
]
