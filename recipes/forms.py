from django import forms 
from . import models

class CreateRecipe(forms.ModelForm):
    class Meta:
        model = models.Recipe
        exclude = ['slug', 'madeby']  # Exclude both slug and madeby
        labels = {
            'recipename': 'Recipe Title',
            'recipetype': 'Category',
            # Other labels remain the same
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Briefly describe your recipe'}),
            'ingredients': forms.Textarea(attrs={'rows': 4, 'placeholder': 'List your ingredients, one per line'}),
            'instructions': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide step-by-step instructions'}),
            # Remove the madeby widget since we're excluding it
        }