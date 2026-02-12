from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage, name='frontpage'),
    path('about/', views.about_view, name='about'),
    path('properties', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('favorite/',views.favorites_list, name='favorite_list'),
    path('<int:pk>/favorite/', views.toggle_favorite,name='toggle_favorite'),
    path('createProperty/', views.create_property, name='create_property'),
    path('property/<int:pk>/update/', views.update_property, name='update_property'),
    path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),
]