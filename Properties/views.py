from django.shortcuts import render
from .models import Properties


def property_list(request):
    properties = Properties.objects.all()
    return render(request, 'Properties/properties_list.html', {'properties': properties})


