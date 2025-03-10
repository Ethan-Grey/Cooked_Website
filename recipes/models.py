from django.db import models

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
    image = models.ImageField(upload_to='recipes/') 
    slug = models.SlugField()
    recipetype = models.ForeignKey(RecipeType, related_name='recipes', on_delete=models.CASCADE) 

    def __str__(self):
        return self.recipename