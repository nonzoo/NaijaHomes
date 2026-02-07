from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Properties
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PropertyForm, PropertyEditForm


def property_list(request):
    properties = Properties.objects.all()
    return render(request, 'Properties/properties_list.html', {'properties': properties})

def property_detail(request, pk):
    property = Properties.objects.get(id=pk)
    return render(request, 'Properties/property_detail.html', {'property': property})

@login_required
@permission_required('Properties.add_properties', raise_exception=True)
def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.agent = request.user
            property.save()
            return redirect('property_detail', pk=property.id)
    else:
        form = PropertyForm()
    return render(request, 'Properties/create_property.html', {'form': form})


@login_required
@permission_required('Properties.change_properties', raise_exception=True)
def update_property(request, pk):
    property = get_object_or_404(Properties, id=pk, agent=request.user)
    if request.method == 'POST':
        form = PropertyEditForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            property = form.save(commit=False)
            property.agent = request.user
            property.save()
            return redirect('property_detail', pk=property.id)
    else:
        form = PropertyEditForm(instance=property)
    return render(request, 'Properties/edit_property.html', {'form': form})


def property_detail(request, pk):
    property = Properties.objects.get(id=pk)
    return render(request, 'Properties/property_detail.html', {'property': property})