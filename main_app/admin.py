from django.contrib import admin

# import
from .models import Recipe, Review, Dish_Type, Photo

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Dish_Type)
admin.site.register(Photo)
