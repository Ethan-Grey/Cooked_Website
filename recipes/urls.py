from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path('new-recipes/', views.new_recipes, name='new_recipes'),
    path('<str:category>/', views.recipe_category, name='category'),
    path('<str:category>/<slug:slug>/', views.recipe_detail, name='detail'),
]