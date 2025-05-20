"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from . import views

#URL Conf
urlpatterns = [
    path('', views.FilesListView.as_view(), name='home'), #How?
    path('upload/', views.UploadFileView.as_view(), name='up'),
    path('download/', views.RetrieveFileView.as_view(), name='down'),
    path('files/', views.FilesListView.as_view(), name='share.files'),
    path('file/<int:pk>', views.FileDetailView.as_view(), name='file.detail'),
    path('file/<int:pk>/edit', views.UpdateFileView.as_view(), name='file.update'),
    path('file/<int:pk>/share', views.RetrieveFileView.as_view(), name='file.share'),
    path('file/retrieve', views.RetrieveFileView.as_view(), name='file.retrieve'),
    path('file/download', views.DownloadFileView.as_view(), name='file.download'),
]
