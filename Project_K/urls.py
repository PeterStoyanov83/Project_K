"""
URL configuration for Project_K project.

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
# urls.py
from django.contrib import admin
from django.urls import path
from clients.views import client_profile_view
from clients import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/clients/client/<int:object_id>/profile/',
         client_profile_view,
         name='clients_client_change'
    ),

    path('admin/clients/client/<int:object_id>/change/',
         views.edit_client_view,
         name='clients_edit_client_change'),
]

app_name = 'clients'
