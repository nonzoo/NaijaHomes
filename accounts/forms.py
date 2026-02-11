from .models import AgentProfile, CustomerProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
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
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'role')

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        if not role:
            raise forms.ValidationError("Please select a role.")

        return cleaned


class EditProfileForm(forms.Form):
    # --- User fields ---
    username = forms.CharField()
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)

    profile_image = forms.ImageField(required=False)

    experience = forms.IntegerField(required=False, min_value=0)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")  
        super().__init__(*args, **kwargs)

        # preload user fields
        self.fields["username"].initial = self.user.username
        self.fields["email"].initial = self.user.email
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["phone_number"].initial = getattr(self.user, "phone_number", "")

        # If user is NOT an agent, remove the agent-only field
        if hasattr(self.user, "agent_profile"):
            self.fields["experience"].initial = self.user.agent_profile.experience
            self.fields["bio"].initial = self.user.agent_profile.bio

        else:
            self.fields.pop("experience")
            self.fields.pop("bio")


    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = User.objects.filter(username__iexact=username).exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            return email
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email


    def save(self):
        # save user fields
        self.user.username = self.cleaned_data["username"]
        self.user.email = self.cleaned_data.get("email", "")
        self.user.first_name = self.cleaned_data.get("first_name", "")
        self.user.last_name = self.cleaned_data.get("last_name", "")

        if hasattr(self.user, "phone_number"):
            self.user.phone_number = self.cleaned_data.get("phone_number", "")

        if self.cleaned_data.get("profile_image"):
            self.user.profile_image = self.cleaned_data["profile_image"]

        self.user.save()

        # save agent-only field
        if hasattr(self.user, "agent_profile") and "experience"  in self.cleaned_data:
            agent = self.user.agent_profile
            agent.experience = self.cleaned_data.get("experience") or 0
            agent.bio = self.cleaned_data.get("bio", "")
            agent.save()

        return self.user