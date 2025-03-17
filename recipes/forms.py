from django import forms 
from . import models
from .models import Review

class CreateRecipe(forms.ModelForm):
    class Meta:
        model = models.Recipe
        exclude = ['slug', 'madeby', 'favorites']  # Exclude both slug and madeby
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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }