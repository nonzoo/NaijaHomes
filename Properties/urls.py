from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('create_property/', views.create_property, name='create_property'),
    path('property/<int:pk>/update/', views.update_property, name='update_property'),
]