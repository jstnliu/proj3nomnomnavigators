from django.contrib import admin

# Register your models here.
from .models import Recipe, Review, Dish_Type, Photo
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Dish_Type)
admin.site.register(Photo)
