from django.shortcuts import render, get_object_or_404
from .models import Client, Course

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/client_detail.html', {'client': client})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'clients/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'clients/course_detail.html', {'course': course})
