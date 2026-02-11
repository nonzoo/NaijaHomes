from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Favorite, Properties
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PropertyForm, PropertyEditForm
from django.db.models import Q
from django.http import JsonResponse


@login_required
def toggle_favorite(request, pk):
    if request.method == "POST":
        prop = get_object_or_404(Properties, id=pk)

        fav = Favorite.objects.filter(user=request.user, property=prop).first()

        if fav:
            fav.delete()
            return JsonResponse({
                "status": "removed",
                "message": "Removed from favorites"
            })
        else:
            Favorite.objects.create(user=request.user, property=prop)
            return JsonResponse({
                "status": "added",
                "message": "Saved to favorites"
            })

    return JsonResponse({"error": "Invalid request"}, status=400)




def frontpage(request):
    featured_properties = Properties.objects.filter(is_featured=True).order_by("-created_at")[:6]
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(
            user=request.user
        ).values_list("property_id", flat=True)

    return render(request, 'Properties/frontpage.html',{'featured_properties':featured_properties,'favorite_ids':favorite_ids})



def property_list(request):
    qs = Properties.objects.all()
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(
            user=request.user
        ).values_list("property_id", flat=True)
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
    return render(request, 'Properties/properties_list.html', {'properties': qs,'favorite_ids':favorite_ids})


def property_detail(request, pk):
    property = Properties.objects.get(id=pk)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, property=property).exists()

    return render(request, 'Properties/property_detail.html', {'property': property,'is_favorited':is_favorited})



@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("property").order_by("-created_at")
    return render(request, "Properties/favorites_list.html", {"favorites": favorites})






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