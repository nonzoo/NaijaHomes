from django.urls import path
from . import views

urlpatterns = [

    path('auth/', views.authView, name="auth"),
    path('selectrole/', views.selectRoleView, name="select_role"),
    path('logout/', views.logoutView, name="logout"),
    path('dashboard/', views.agent_dashboard, name="agent_dashboard"),
    path('myprofile/',views.profile_view, name='my_profile'),
    path('updateprofile/',views.update_profile, name='update_profile'),
    path('agents/', views.agentsView, name='agents_list'),
    path('agent/<int:agent_id>/', views.agent_profile_view, name='agent_profile'),
]

# path('customer_dashboard/', views.customer_dashboard, name="customer_dashboard"),    
# path('signup/', views.signupView, name="signup"),
# path('login/', views.loginView, name="login"),