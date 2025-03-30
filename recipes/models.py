from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg

# Create your models here.

class RecipeType(models.Model):
    recipetype = models.CharField(max_length=100)

    def __str__(self):
        return self.recipetype
    

class Recipe(models.Model):
    recipename = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    prep_time = models.IntegerField(help_text="Preparation time in minutes", default=0)
    cook_time = models.IntegerField(help_text="Cooking time in minutes", default=0)
    servings = models.IntegerField(help_text="Number of servings", default=1)
    
    # Change this line to use ForeignKey instead of CharField
    madeby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    
    image = models.ImageField(upload_to='recipes/')
    slug = models.SlugField(blank=True)
    recipetype = models.ForeignKey(RecipeType, related_name='recipes', on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.recipename)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.recipename
    
    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            return round(avg)
        return 0


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe']  # Ensures one review per user per recipe

    def __str__(self):
        return f'Review by {self.user.username} on {self.recipe.recipename}'