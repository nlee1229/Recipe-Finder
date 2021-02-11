from django.db import models
from login_reg.models import User


class Recipe(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    level = models.IntegerField() 
    cooktime = models.CharField(max_length = 255)
    instructions = models.TextField() 
    user_recents = models.ManyToManyField(User, related_name="recents")
    user_favs = models.ManyToManyField(User, related_name="favorites")
    created_by = models.ForeignKey(User, related_name="createdby", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    img = models.ImageField(upload_to="gallery", height_field=None, width_field=None)
    recipe_img = models.ForeignKey(Recipe, related_name="recipe_imgs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    name = models.CharField(max_length = 20)
    qty = models.CharField(max_length = 255)
    unit = models.CharField(max_length = 255)
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


