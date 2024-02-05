#
# URL configuration for Project_K project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

# urls.py
from django.contrib import admin
from django.urls import path, include

from clients import views

urlpatterns = [
    path('client/<int:object_id>/change/', views.client_profile_view, name='client_profile_view'),

    path('admin/', admin.site.urls),

    path('clients/', include(('clients.urls', 'clients'), namespace='clients')),
]

app_name = 'clients'
