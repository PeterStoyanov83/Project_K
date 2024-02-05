# views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Client
from .forms import ClientForm


@login_required  # Only logged-in users can view client profiles
def client_profile_view(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    context = {'client': client}
    return render(request, 'clients/client_profile.html', context)


@login_required  # Only logged-in users can edit client profiles
def edit_client_view(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_profile', object_id=client.id)  # Updated redirect URL
    else:
        form = ClientForm(instance=client)
    context = {'form': form, 'client': client}
    return render(request, 'clients/edit_client.html', context)


@method_decorator(login_required, name='dispatch')  # Only logged-in users can view client details
class ClientDetailView(View):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('pk')
        client = get_object_or_404(Client, pk=client_id)

        # Here, we'll just check if the user is authenticated.
        # You could expand this to check for specific permissions or roles.
        if not request.user.is_authenticated:
            raise Http404("You do not have permission to view this client's files.")

        # Fetch the client files associated with this client
        client_files = client.files.all()

        # Render the client detail template with the client and files
        context = {'client': client, 'client_files': client_files}
        return render(request, 'clients/client_detail.html', context)