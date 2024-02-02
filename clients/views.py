# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientForm
from .models import Client


def client_profile_view(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    context = {'client': client}
    return render(request, 'clients/client_profile.html', context)


def edit_client_view(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:client_profile_view', object_id=client.id)  # Updated redirect URL
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/edit_client.html', {'form': form})
