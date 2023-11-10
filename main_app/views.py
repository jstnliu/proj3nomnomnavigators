import uuid
import boto3
import os
import requests
import json
from django.http import HttpResponseBadRequest
from django.db.models import Q
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
from .models import Recipe, Nutrition_Label, Photo, Nutrient
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
def recipes_user(request):
    recipes = Recipe.objects.filter(user = request.user)
    return render(request, 'recipes/user.html', {
        'recipes': recipes 
    })

#   ENTIRE INDEX
@login_required
def recipes_all(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    recipes = Recipe.objects.filter(
        Q(name__icontains=query) |  # Search in name
        Q(ingredients__icontains=query) |  # Search in ingredients
        Q(description__icontains=query)  # Search in description
    )
    context = {
        'recipes': recipes,
        'query': query,  # Pass the query back to the template for display
    }
    return render(request, 'recipes/index.html', context)

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
    recipe = Recipe.objects.get(id=recipe_id)

    # Check if the recipe already has a nutrition label
    if recipe.nutrition_label:
        # If it does, update the existing nutrition label
        nutrition_label = recipe.nutrition_label
    else:
        # If not, create a new nutrition label
        nutrition_label = Nutrition_Label()

    ingredients_list = recipe.get_ingredients_list()
    url = "https://api.edamam.com/api/nutrition-details?app_key=fa795efd1a20b3360e47f10934c667ab&app_id=27c6d9ed"

    payload = json.dumps({
        "title": f"{recipe.name}",
        "ingr": ingredients_list,
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # Send request to Edamam API
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        # Parse the response and update Nutrition_Label instance
        nutrition_data = json.loads(response.text)

        nutrition_label.yield_value = nutrition_data.get('yield', 1.0)
        nutrition_label.calories = nutrition_data['calories']
        nutrition_label.total_fats = nutrition_data.get('total_fats', 0.0)
        nutrition_label.cholesterol = nutrition_data.get('cholesterol', 0.0)
        nutrition_label.sodium = nutrition_data.get('sodium', 0.0)
        nutrition_label.total_carbs = nutrition_data.get('total_carbs', 0.0)
        nutrition_label.protein = nutrition_data.get('protein', 0.0)
        # Update or create nutrients
        nutrients = nutrition_data.get('totalNutrients', {})
        nutrition_label.user = request.user
        nutrition_label.save()

        # Associate the Nutrition_Label with the Recipe
        recipe.nutrition_label = nutrition_label
        recipe.save()

        # Associate nutrients with Nutrition_Label
        for nutrient_label, nutrient_data in nutrients.items():
            nutrient, created = Nutrient.objects.get_or_create(
                label=nutrient_label,
                defaults={'quantity': nutrient_data.get('quantity', 0.0), 'unit': nutrient_data.get('unit', '')}
            )
            nutrition_label.nutrients.add(nutrient)

    else:
        # If the API request is not successful, return a bad request response
        return HttpResponseBadRequest(response.text)

    return redirect('detail', recipe_id=recipe_id)
# # work on feeding actual food ing into payload
#     recipe = Recipe.objects.get(id = recipe_id)
#     ingredients_list = recipe.get_ingredients_list()
#     url = "https://api.edamam.com/api/nutrition-details?app_key=fa795efd1a20b3360e47f10934c667ab&app_id=27c6d9ed"

#     payload = json.dumps({
#     "title": f"{recipe.name}",
#     "ingr": ingredients_list,
#     })
#     headers = {
#     'Content-Type': 'application/json'
#     }
# # send response to detail.html
#     response = requests.request("POST", url, headers=headers, data=payload)

#     if response.status_code == 200:
#             # Parse the response and create a Nutrition_Label instance
#             nutrition_data = json.loads(response.text)
#             nutrition_label = Nutrition_Label.objects.create(
#                 calories=nutrition_data['calories'],
#                 # Add other fields based on your JSON structure
#                 user=request.user  # or whatever logic you use to get the user
#             )
#             # Associate the Nutrition_Label with the Recipe
#             recipe.nutrition_label = nutrition_label
#             recipe.save()

#     print(response.text)
#     return redirect('detail', recipe_id = recipe_id) 
