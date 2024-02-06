# clients/urls.py

from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # Path for the read-only client profile view
    path('<int:object_id>/', views.client_profile_view, name='client_profile_view'),

    # Path for the editable client profile view
    path('<int:object_id>/edit/', views.edit_client_view, name='edit_client_change'),

    # Path for the detailed client view (if this is different from the above view-only profile)
    path('<int:pk>/detail/', views.ClientDetailView.as_view(), name='client_detail'),
]

