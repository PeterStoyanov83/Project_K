from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import Http404
from .models import Client

@login_required  # Only logged-in users can view client profiles
def client_profile_view(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    context = {'client': client, 'edit': False}  # 'edit': False to indicate view-only mode
    return render(request, 'clients/client_profile.html', context)

@login_required  # Only logged-in users can edit client profiles
def edit_client_view(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:client_profile_view', object_id=client.id)
    else:
        form = ClientForm(instance=client)
    context = {'form': form, 'client': client}
    return render(request, 'clients/client_edit.html', context)

class ClientDetailView(View):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('pk')
        client = get_object_or_404(Client, pk=client_id)

        # Check if the user has permission to view this client's details
        # Implement your own permission logic here
        if not request.user.has_perm('can_view_client', client):
            raise Http404("You do not have permission to view this client's files.")

        # Fetch the client files associated with this client
        client_files = client.files.all()

        # Render the client detail template with the client and files
        return render(request, 'clients/client_detail.html', {'client': client, 'client_files': client_files})
