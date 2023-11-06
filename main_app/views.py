
from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# home view
def home(request):
    # include .html file extension 
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def recipes_index(request):
  recipes = Recipe.objects.filter(user=request.user)
  return render(request, 'recipes/index.html', {
    'recipes': recipes
  })

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