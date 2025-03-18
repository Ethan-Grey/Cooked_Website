from django.contrib import admin
from .models import Recipe, RecipeType, Review

# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecipeType)
admin.site.register(Review)