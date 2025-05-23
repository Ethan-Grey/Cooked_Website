from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path('new-recipes/', views.new_recipes, name='new_recipes'),
    path('all-recipes/', views.all_recipes, name='all_recipes'),
    path('recipe/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('search/', views.search, name='search'),
    path('favorite/<int:recipe_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('unfavorite/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    # Generic patterns with string/slug parameters should come last
    path('recipe/<int:recipe_id>/review/', views.add_review, name='add_review'),
    path('<str:category>/', views.recipe_category, name='category'),
    path('<str:category>/<slug:slug>/', views.recipe_detail, name='detail'),
    path('recipe/<int:recipe_id>/remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:recipe_id>/add/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
]