from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Properties
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PropertyForm, PropertyEditForm
from django.db.models import Q


def property_list(request):
    qs = Properties.objects.all()

    q = request.GET.get("q")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(address__icontains=q) |
            Q(description__icontains=q)
        )

    if min_price:
        qs = qs.filter(price__gte=min_price)

    if max_price:
        qs = qs.filter(price__lte=max_price)
    return render(request, 'Properties/properties_list.html', {'properties': qs})


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


@login_required
@permission_required('Properties.delete_properties', raise_exception=True)
def delete_property(request, pk):
    property = get_object_or_404(Properties, id=pk, agent=request.user)

    if request.method == 'POST':
        property.delete()
        return redirect('property_list')
    
    return render(request, 'Properties/confirm_delete.html', {'property':property})