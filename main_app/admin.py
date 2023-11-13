from django.contrib import admin

# import
from .models import Recipe, Review, Photo

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Review)
# FUTURE USE IMPLEMENTATION
# admin.site.register(Dish_Type)
admin.site.register(Photo)
