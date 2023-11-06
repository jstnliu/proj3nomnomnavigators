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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

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
    
