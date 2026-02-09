from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signupView, name="signup"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('agent_dashboard/', views.agent_dashboard, name="agent_dashboard"),
    path('customer_dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('my_profile/',views.profile_view, name='my_profile'),
    path('updateprofile/',views.update_edit, name='update_profile')
]