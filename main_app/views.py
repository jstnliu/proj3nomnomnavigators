import uuid
# import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# UserCreationForm that we can use in a template to generate all of the inputs for a User model.
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# models imports
from .models import Recipe, Dish_Type, Photo

# home view
def home(request):
    # include .html file extension 
    return render(request, 'home.html')

# user req
def about(request):
    return render(request, 'about.html')

# user req
def recipes_index(request):
    recipes = Recipe.objects.filter(user = request.user)
    return render(request, 'recipes/index.html', {
        'recipes': recipes 
    })

# user req
def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    # list of of dish_type ids that recipe DOES have
    id_list = recipe.dish_types.all().values_list('id')
    # query for dish_types cat DOESN'T have
    # by using exclude() method 
    dish_types_recipe_doesnt_have = Dish_Type.objects.exclude(id_in = id_list)
    review_form = ReviewForm()
    return render(request, 'recipes/detail.html', )


