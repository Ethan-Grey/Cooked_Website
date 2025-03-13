from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.hashers import make_password

def prepare_madeby_field(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    User = apps.get_model('auth', 'User')
    
    # Get or create a default user to assign recipes with invalid usernames
    default_user, created = User.objects.get_or_create(
        username='recipe_system',
        defaults={
            'email': 'system@example.com',
            'is_active': True,
            'password': make_password('temporarypassword')  # Use make_password instead of set_password
        }
    )
    
    # Update all recipes to use a valid username that exists
    for recipe in Recipe.objects.all():
        try:
            # Try to find a user with this username
            username = recipe.madeby
            user = User.objects.get(username=username)
            # If found, keep the username as is
        except User.DoesNotExist:
            # If not found, set to the default username
            recipe.madeby = default_user.username
            recipe.save()

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipe_slug'),  # Keep your correct previous migration
    ]

    operations = [
        migrations.RunPython(prepare_madeby_field),
    ]