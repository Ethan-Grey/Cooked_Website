from django.shortcuts import render
from .models import Recipe, RecipeType

# Create your views here.
def breakfast(request):
    recipe_type = RecipeType.objects.get(recipetype="Breakfast")
    breakfast_recipes = recipe_type.recipes.all()
    return render(request, 'recipes/breakfast.html', {'breakfast_recipes': breakfast_recipes})
