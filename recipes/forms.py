from django import forms 
from . import models
from .models import Review

class CreateRecipe(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ['recipename', 'description', 'ingredients', 'instructions', 'prep_time', 'cook_time', 'servings', 'image', 'recipetype']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter each ingredient on a new line'}),
            'instructions': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter each step on a new line'}),
            'prep_time': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Prep time in minutes'}),
            'cook_time': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Cook time in minutes'}),
            'servings': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Number of servings'})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }