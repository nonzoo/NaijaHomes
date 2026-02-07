from .models import Properties
from django import forms

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields = ['title', 'price', 'address', 'description', 'image']


class PropertyEditForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields = ['title', 'price', 'address', 'description', 'image']

