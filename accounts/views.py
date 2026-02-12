from django.shortcuts import get_object_or_404, render,redirect
from .forms import SignUpForm,EditProfileForm
from django.contrib.auth import login, authenticate,logout
from .models import AgentProfile, CustomerProfile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from Properties.models import Properties
from django.contrib import messages
from django.core.paginator import Paginator


def authView(request):
    
    if request.user.is_authenticated:
        return redirect("my_profile")

    signup_form = SignUpForm()
    login_error = None

    if request.method == "POST":
        action = request.POST.get("action")


        if action == "login":
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # redirect based on group

                return redirect("my_profile")

            login_error = "Invalid username or password."


        elif action == "signup":
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                role = signup_form.cleaned_data.get("role")

                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)
                if role == "Agent":
                    AgentProfile.objects.create(
                        user=user,
                        
                    )
                    redirect_name = "my_profile"
                else:
                    CustomerProfile.objects.create(
                        user=user,
                        
                    )
                    redirect_name = "my_profile"


                login(request, user)
                return redirect(redirect_name)

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



# @login_required
# @permission_required('accounts.view_customerprofile', raise_exception=True)
# def customer_dashboard(request):
#     customer = get_object_or_404(CustomerProfile, user=request.user)
#     return render(request, "accounts/customer_dashboard.html", {'customer':customer})


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


def agentsView(request):
    agents_list = AgentProfile.objects.all()
    paginator = Paginator(agents_list, 8)  # 8 agents per page
    page_number = request.GET.get('page')
    agents = paginator.get_page(page_number)
    return render(request, "accounts/agents.html", {"agents": agents})


def agent_profile_view(request, agent_id):
    """View a specific agent's public profile and their properties"""
    agent = get_object_or_404(AgentProfile, user__id=agent_id)
    properties_list = Properties.objects.filter(agent__id=agent_id)
    featured_count = properties_list.filter(is_featured=True).count()
    
    # Pagination
    paginator = Paginator(properties_list, 6)  # 6 properties per page
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)
    
    return render(request, "accounts/agent_profile.html", {
        'agent': agent,
        'properties': properties,
        'featured_count': featured_count,
        'agent_user': agent.user
    })