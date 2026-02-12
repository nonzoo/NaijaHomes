from .models import Properties
from django import forms

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields = ['title', 'price', 'address','state', 'description', 'image', 'property_type', 'bedrooms', 'living_rooms', 'bathrooms', 'Sqm']


class PropertyEditForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields = ['title', 'price', 'address','state', 'description', 'image', 'property_type', 'bedrooms', 'living_rooms', 'bathrooms', 'Sqm']

