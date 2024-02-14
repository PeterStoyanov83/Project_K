# clients/urls.py

from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),

]
