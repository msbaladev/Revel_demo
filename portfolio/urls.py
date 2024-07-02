from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns=[
    path("",home,name="home"),
    path("signin/",signin,name="signin"),
    path("file-upload/",file_upload,name="file-upload"),
    path('QP_iness_bulk_upload/', QP_iness_bulk_upload, name='QP_iness_bulk_upload'),
    path('qp_bulk_attchments/', qp_bulk_attchments, name="qp_bulk_attchments"),
    path('download_Iness_reval_bulkapproval/',download_Iness_bulkapproval,name="download_Iness_bulkapproval"),
    path("bulk_files/",bulk_files,name="bulk_files"),
    path("downloadmdfile/<int:id>/",downloadmdfile,name="downloadmdfile"),
    path('reval_data/',reval_data,name="reval_data")
      
  
]