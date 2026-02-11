from django.shortcuts import get_object_or_404, render,redirect
from .forms import SignUpForm,EditProfileForm
from django.contrib.auth import login, authenticate,logout
from .models import AgentProfile, CustomerProfile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from Properties.models import Properties
from django.contrib import messages


def authView(request):
    # If already logged in, send them to the right dashboard
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Agent").exists():
            return redirect("agent_dashboard")
        return redirect("customer_dashboard")

    signup_form = SignUpForm()
    login_error = None

    if request.method == "POST":
        action = request.POST.get("action")

        # ---------- LOGIN ----------
        if action == "login":
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # redirect based on group

                return redirect("my_profile")

            login_error = "Invalid username or password."

        # ---------- SIGNUP ----------
        elif action == "signup":
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                role = signup_form.cleaned_data.get("role")

                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)


                login(request, user)
                return redirect('my_profile')

        # If action missing, just stay on page

    return render(
        request,
        "accounts/auth.html",
        {
            "form": signup_form,
            "login_error": login_error,
        },
    )




def logoutView(request):
    logout(request)
    return redirect('auth')


@login_required
@permission_required('accounts.view_agentprofile', raise_exception=True)
def agent_dashboard(request):
    agent = get_object_or_404(AgentProfile, user=request.user)
    property = Properties.objects.filter(agent=request.user)
    featured_count = property.filter(is_featured=True).count()
    
    return render(request, "accounts/agent_dashboard.html",{'agent' : agent, 'properties': property, 'featured_count': featured_count})



@login_required
@permission_required('accounts.view_customerprofile', raise_exception=True)
def customer_dashboard(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    return render(request, "accounts/customer_dashboard.html", {'customer':customer})


@login_required
def profile_view(request):
    if request.user.groups.filter(name='Agent').exists():
        agent = get_object_or_404(AgentProfile, user=request.user)
        context = {'agent':agent}
    else:
        customer = get_object_or_404(CustomerProfile, user=request.user)
        context = {'customer':customer}
    return render(request, 'accounts/profile.html',context)



@login_required
def update_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST,request.FILES, user=request.user)
        if form.is_valid():
            form.save() 
            
            return redirect("my_profile")
        messages.success(request, "Profile updated successfully!")
    else:
        form = EditProfileForm(user=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})


 