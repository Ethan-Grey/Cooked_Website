from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class RecipeType(models.Model):
    recipetype = models.CharField(max_length=100)

    def __str__(self):
        return self.recipetype
    

class Recipe(models.Model):
    recipename = models.CharField(max_length=200)
    description = models.TextField() 
    ingredients = models.TextField() 
    instructions = models.TextField(default='No instructions provided')
    madeby = models.CharField(max_length=50, default='Firstname Lastname')
    # madeby = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='recipes/') 
    slug = models.SlugField()
    recipetype = models.ForeignKey(RecipeType, related_name='recipes', on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.recipename)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.recipename