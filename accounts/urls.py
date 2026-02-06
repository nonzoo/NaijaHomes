from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/', views.signupView, name="signup"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('agent_dashboard/', views.agent_dashboard, name="agent_dashboard"),
    path('customer_dashboard/', views.customer_dashboard, name="customer_dashboard"),
]