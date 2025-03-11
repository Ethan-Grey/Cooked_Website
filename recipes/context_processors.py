from .models import RecipeType, Recipe

def recipe_types(request):
    return {'recipe_types': RecipeType.objects.all()}

def recipes(request):
    return {'recipes': Recipe.objects.all()}