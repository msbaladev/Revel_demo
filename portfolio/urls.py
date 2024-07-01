from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns=[
    path("",home,name="home"),
    path("signin/",signin,name="signin"),
    path("file-upload/",file_upload,name="file-upload"),
    path('reval_data/', reval_data, name='reval_data'),
     
    path('download_Iness_reval_bulkapproval/',download_Iness_bulkapproval,name="download_Iness_bulkapproval"),
  
]