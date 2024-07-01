from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns=[
    path("",home,name="home"),
    path("signin/",signin,name="signin"),
    path("file-upload/",file_upload,name="file-upload"),
    path('api/items/', item_list, name='item_list'),
]