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
# class Dish_Type(models.Model):
#     cuisine = models.CharField(max_length = 50)
#     diet = models.CharField(max_length = 50)
    
#     def __str__(self):
#         return self.name
    
#     def get_absolute_url(self):
#         return reverse('dish_types_detail', kwargs = {
#             'pk': self.id
#         })

class Nutrient(models.Model):
    label = models.CharField(max_length=50)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)
    
# EDAMAM API Model (incomplete)
# create a model for label
# get what we want from response
# what attributes for model Label we want are from response 
# in html
    # recipe.nutrition_label.attr
class Nutrition_Label(models.Model):
    recipe_uri = models.URLField(default = 'UNKNOWN_RECIPE_URI')
    yield_value = models.FloatField(default = 1.0)
    calories = models.FloatField(default = 0.0)
    total_fat = models.FloatField(default = 0.0)
    saturated_fat = models.FloatField(default = 0.0)
    trans_fat = models.FloatField(default = 0.0)
    cholesterol = models.FloatField(default = 0.0)
    sodium = models.FloatField(default = 0.0)
    dietary_fiber = models.FloatField(default = 0.0)
    protein = models.FloatField(default = 0.0)
    total_carbs = models.FloatField(default = 0.0)
    total_sugars = models.FloatField(default = 0.0)
    # added_sugars = models.FloatField(default = 0.0)
    nutrients = models.ManyToManyField(Nutrient)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def save(self, *args, **kwargs):
        # If yield_value is not provided, set it to the serving_size of the associated Recipe
        if not self.yield_value and self.recipe:
            self.yield_value = self.recipe.serving_size
        
        # Round the float fields to two decimal places before saving
        self.calories = round(self.calories, 2)
        self.total_fat = round(self.total_fat, 2)
        self.saturated_fat = round(self.saturated_fat, 2)
        self.trans_fat = round(self.trans_fat, 2)
        self.cholesterol = round(self.cholesterol, 2)
        self.sodium = round(self.sodium, 2)
        self.dietary_fiber = round(self.dietary_fiber, 2)
        self.protein = round(self.protein, 2)
        self.total_carbs = round(self.total_carbs, 2)
        self.total_sugars = round(self.total_sugars, 2)
        super().save(*args, **kwargs)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Recipe(models.Model):
    name = models.CharField(max_length = 75)
    serving_size = models.FloatField(default = 1.0)
    ingredients = models.TextField(blank = True)
    description = models.TextField()
    directions = models.TextField()
    # One:One relation with Nutrition Label
    nutrition_label = models.OneToOneField(Nutrition_Label, on_delete=models.CASCADE, null=True, blank=True)
    # M:M relation tie-in
    # dish_types = models.ManyToManyField(Dish_Type)
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



