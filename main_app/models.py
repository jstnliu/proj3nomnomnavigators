from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

RATINGS = (
    ('1', 'I wouldn\'t trust them running a bath, let alone a restaurant.'),
    ('2', 'This isn\'t a recipe, this is a mistake.'),
    ('3', 'They\'re not afraid to take risks, and they\'re not afraid to fail; that\'s how you succeed.'),
    ('4', 'I believe that if they worked hard, stay focused, and never give up, they can achieve anything.'),
    ('5', 'Chefs are like magicians, they transform raw ingredients into something magical.'),
)

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
    # label = 
    # M:M relation tie-in
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
        return f'{self.name} ({self.id})'       


    def get_absolute_url(self):
        return reverse('detail', kwargs = {
            'recipe_id': self.id
        })

    # def reviewed_for_today(self):
    #     return self.review_set.filter(date = date.today()).count()
    
class Review(models.Model):
    date = models.DateField('Date Posted')
    rating = models.CharField(
        max_length = 1,
        choices = RATINGS,
        default = RATINGS[2][0],
    )
    comment = models.TextField(
        max_length = 200,
    )
    # create recipe_id FK
    recipe = models.ForeignKey(
        Recipe, 
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f'{self.get_rating_display()} and {self.get_comment_display()} on {self.date}'
    
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length = 200)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)

    def __str__(self):
        return f'Photo for recipe_id: {self.recipe_id} @{self.url}'

# EDAMAM API Model (incomplete)
# probably have to import stuff for it later on
# create a model for label
# get what we want from response
# what attributes for model Label we want are from response 
# in html
    # recipe.label.attr
class Nutrition_Label(models.Model):
    calories = models.IntegerField()
    total_fats = models.IntegerField()
    cholesterol = models.IntegerField()
    sodium = models.IntegerField()
    total_carbs = models.IntegerField()
    protein = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)

