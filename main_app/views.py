import uuid
import boto3
import os
import requests
import json
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
from .forms import ReviewForm

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

# @login_required
# def about(request):
#     return render(request, 'about.html')

@login_required
def recipes_index(request):
    recipes = Recipe.objects.filter(user = request.user)
    return render(request, 'recipes/index.html', {
        'recipes': recipes 
    })

@login_required
def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    # list of of dish_type ids that recipe DOES have
    # id_list = recipe.dish_types.all().values_list('id')
    # query for dish_types cat DOESN'T have
    # by using exclude() method 
    # dish_types_recipe_doesnt_have = Dish_Type.objects.exclude(id_in = id_list)
    review_form = ReviewForm()
    return render(request, 'recipes/detail.html', {
       'recipe': recipe,
       'review_form': review_form,
    #    'dish_types': dish_types_recipe_doesnt_have,
    })

class RecipeCreate(LoginRequiredMixin, CreateView):
   model = Recipe
   fields = [
      'name',
      'serving_size',
      'ingredients',
      'description',
      'directions',
    ]

   def form_valid(self, form):
    #   assign logged-in user (self.request.user)
    # form.instace is recipe
      form.instance.user = self.request.user
      return super().form_valid(form)
   
   
class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = [
        'name',
        'serving_size',
        'ingredients',
        'description',
        'directions',
    ]

class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/recipes'

@login_required
def add_review(request, recipe_id):
    # create ModelForm instance using
    # data submitted in form
    form = ReviewForm(request.POST)
    # validate form
    if form.is_valid():
        # assign recipe_id FK
        new_recipe = form.save(commit = False)
        new_recipe.recipe_id = recipe_id
        new_recipe.save()
    return redirect('detail', recipe_id = recipe_id)

class Dish_TypeList(LoginRequiredMixin, ListView):
   model = Dish_Type

class Dish_TypeDetail(LoginRequiredMixin, DetailView):
   model = Dish_Type

class Dish_TypeCreate(LoginRequiredMixin, CreateView):
   model = Dish_Type
   fields = '__all__'

class Dish_TypeUpdate(LoginRequiredMixin, UpdateView):
   model = Dish_Type
   fields = [
      'cuisine',
      'diet'
    ]

class Dish_TypeDelete(LoginRequiredMixin, DeleteView):
   model = Dish_Type
   success_url = '/dish_types'

@login_required
def assoc_dish_type(request, recipe_id, dish_type_id):
   Recipe.objects.get(id = recipe_id).dish_types.add(dish_type_id)
   return redirect('detail', recipe_id = recipe_id)

@login_required
def unassoc_dish_type(request, recipe_id, dish_type_id):
   Recipe.objects.get(id = recipe_id).dish_types.remove(dish_type_id)
   return redirect('detail', recipe_id = recipe_id)

@login_required
def add_photo(request, recipe_id):
    # photo-file will be the 'name' attribute on <input type = 'file'>
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # safety measure for something going wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to recipe_id or recipe (if you have a recipe object)
            Photo.objects.create(url = url, recipe_id = recipe_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', recipe_id = recipe_id)
       
def label_create(request, recipe_id):
# work on feeding actual food ing into payload
    recipe = Recipe.objects.get(id = recipe_id)
    ingredients_list = recipe.get_ingredients_list()
    url = "https://api.edamam.com/api/nutrition-details?app_key=fa795efd1a20b3360e47f10934c667ab&app_id=27c6d9ed"

    payload = json.dumps({
    "title": f"{recipe.name}",
    "ingr": ingredients_list,
    })
    headers = {
    'Content-Type': 'application/json'
    }
# send response to detail.html
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return redirect('detail', recipe_id = recipe_id) 
