# Generated by Django 5.1.7 on 2025-03-11 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_review_savedrecipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedrecipe',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='savedrecipe',
            name='user',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='SavedRecipe',
        ),
    ]
