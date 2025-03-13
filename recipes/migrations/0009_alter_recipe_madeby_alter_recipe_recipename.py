from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

def link_users_to_recipes(apps, schema_editor):
    """
    Link each recipe to its user via the foreign key relationship
    """
    Recipe = apps.get_model('recipes', 'Recipe')
    User = apps.get_model('auth', 'User')
    
    # For each recipe, find the corresponding user and set the foreign key
    for recipe in Recipe.objects.all():
        username = recipe.madeby  # The current string username
        try:
            user = User.objects.get(username=username)
            recipe.user = user  # Set the new foreign key relationship as a temporary field
            recipe.save()
        except User.DoesNotExist:
            # Fall back to system user if any issues
            system_user = User.objects.get(username='recipe_system')
            recipe.user = system_user
            recipe.save()

def reverse_link_users_to_recipes(apps, schema_editor):
    """
    Restore username strings from the foreign key relationship
    """
    Recipe = apps.get_model('recipes', 'Recipe')
    
    for recipe in Recipe.objects.all():
        if recipe.user:
            recipe.madeby = recipe.user.username
            recipe.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_prepare_madeby_for_foreign_key'),
    ]

    operations = [
        # 1. Rename the old field to avoid conflict
        migrations.RenameField(
            model_name='Recipe',
            old_name='madeby',
            new_name='madeby_old',
        ),
        
        # 2. Add the new foreign key field
        migrations.AddField(
            model_name='Recipe',
            name='madeby',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
        
        # 3. Add temporary field for migration
        migrations.AddField(
            model_name='Recipe',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        
        # 4. Run the function to populate the temporary foreign key field
        migrations.RunPython(link_users_to_recipes, reverse_link_users_to_recipes),
        
        # 5. Copy from temporary field to actual field
        migrations.RunSQL(
            "UPDATE recipes_recipe SET madeby_id = user_id WHERE user_id IS NOT NULL",
            "UPDATE recipes_recipe SET madeby_old = '' WHERE madeby_id IS NOT NULL"
        ),
        
        # 6. Make the foreign key field non-nullable
        migrations.AlterField(
            model_name='Recipe',
            name='madeby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
        
        # 7. Remove the temporary fields
        migrations.RemoveField(
            model_name='Recipe',
            name='user',
        ),
        migrations.RemoveField(
            model_name='Recipe',
            name='madeby_old',
        ),
    ]