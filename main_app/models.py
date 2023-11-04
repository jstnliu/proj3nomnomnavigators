from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Dish_Type(models.Model):
    cuisine = models.CharField(max_length = 50)
    diet = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('dish_types_detail', kwargs = {
            'pk': self.id
        })

class Recipe(models.Model):
    name = models.CharField(max_length = 75)
    serving_size = models.CharField(max_length = 75)
    ingredients = models.TextField(blank = True)
    description = models.TextField()
    directions = models.TextField()
    dish_types = models.ManyToManyField(Dish_Type)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def add_ingredient(self, ingredient):
        if not self.ingredients:
            self.ingredients = ingredient
        else: 
            self.ingredients += f', {ingredient}'
        self.save()

    def delete_ingredient(self, ingredient):
        if self.ingredients:
            ingredients_list = [i.remove() for i in self.ingredients.split(', ')]
            if ingredient in ingredients_list:
                ingredients_list.remove(ingredient)
                self.ingredients = ', '.join(ingredients_list)
                self.save()

    def get_ingredients_list(self):
            if self.ingredients:
                return [ingredient.strip() for ingredient in self.ingredients.split(",")]
            else:
                return []

    def __str__(self):
        return self.title       

    def get_absolute_url(self):
        return reverse('detail', kwargs = {
            'recipe_id': self.id
    })      

class Photo(models.Model):
    url = models.CharField(max_length = 200)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)

# # EDAMAM API Model (incomplete)
# # probably have to import stuff for it later on
# class Nutrition_Label(models.Model):
#     calories = models.IntegerField()
#     total_fats = models.IntegerField()
#     cholesterol = models.IntegerField()
#     sodium = models.IntegerField()
#     total_carbs = models.IntegerField()
#     protein = models.IntegerField()
#     user = models.ForeignKey(User, on_delete = models.CASCADE)

