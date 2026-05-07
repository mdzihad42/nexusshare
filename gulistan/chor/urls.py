from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sync/', views.sync, name='sync'),
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('update/<int:file_id>/', views.update_file, name='update_file'),
]
