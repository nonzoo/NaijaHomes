from django.shortcuts import get_object_or_404, render,redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate,logout
from .models import AgentProfile, CustomerProfile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required





def signupView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")

            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            if role == "Agent":
                AgentProfile.objects.create(
                    user=user,
                    
                )
                redirect_name = "agent_dashboard"
            else:
                CustomerProfile.objects.create(
                    user=user,
                    
                )
                redirect_name = "customer_dashboard"

            login(request, user)
            return redirect(redirect_name)
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Agent').exists():
                return redirect('agent_dashboard')
            else:
                return redirect('customer_dashboard')
            
            
    return render(request, 'accounts/login.html')


def logoutView(request):
    logout(request)
    return redirect('login')


@login_required
@permission_required('accounts.view_agentprofile', raise_exception=True)
def agent_dashboard(request):
    agent = get_object_or_404(AgentProfile, user=request.user)
    return render(request, "accounts/agent_dashboard.html",{'agent' : agent})



@login_required
@permission_required('accounts.view_customerprofile', raise_exception=True)
def customer_dashboard(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    return render(request, "accounts/customer_dashboard.html", {'customer':customer})
 