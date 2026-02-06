from .models import AgentProfile, CustomerProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):

    ROLE_CHIOICES = (
        ('', 'Select Role'),
        ('Agent', 'Agent'),
        ('Customer', 'Customer')
        )
    
    role = forms.ChoiceField(choices=ROLE_CHIOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        if not role:
            raise forms.ValidationError("Please select a role.")

        return cleaned

