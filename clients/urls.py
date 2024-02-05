# clients/urls.py
from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path(
        '<int:object_id>/change/',
        views.client_profile_view,
        name='client_profile_view'
    ),
    path(
        '<int:object_id>/edit/',
        views.edit_client_view,
        name='edit_client_change'
    ),
    # Add the detail view URL
    path(
        '<int:pk>/detail/',
        views.ClientDetailView.as_view(),
        name='client_detail'
    ),
]
