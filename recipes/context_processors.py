from .models import RecipeType, Recipe, Review

def recipe_types(request):
    return {'recipe_types': RecipeType.objects.all()}

def reviews(request):
    return {'recent_reviews': Review.objects.select_related('user', 'recipe').order_by('-created_at')[:4]}

def recipes(request):
    return {'recipes': Recipe.objects.all()}

def recipe_categories(request):
    return {
        'filtered_recipe_types': RecipeType.objects.filter(
            recipetype__in=['Breakfast', 'Lunch', 'Dinner', 'Drinks', 'Desserts']     
        ),
        'health_filtered_recipe_types': RecipeType.objects.filter(          # filter for categories in recipetype model
            recipetype__in=["Keto", 'Vegetarian']
        ),
        'holidays_filtered_recipe_types': RecipeType.objects.filter(
            recipetype__in=["Mother's Day", 'New Years']
        ),
    }
