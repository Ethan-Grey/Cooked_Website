from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path('new-recipes/', views.new_recipes, name='new_recipes'),
    path('all-recipes/', views.all_recipes, name='all_recipes'),
    path('edit/<int:pk>/', views.edit_recipe, name='edit'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    # Generic patterns with string/slug parameters should come last
    path('<str:category>/', views.recipe_category, name='category'),
    path('<str:category>/<slug:slug>/', views.recipe_detail, name='detail'),
]