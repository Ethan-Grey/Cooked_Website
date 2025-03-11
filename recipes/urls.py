from django.urls import path
from . import views
app_name = "recipes"

urlpatterns = [
    path('breakfast/', views.breakfast),
    path('new-recipes/', views.new_recipes, name='new_recipes'),
]