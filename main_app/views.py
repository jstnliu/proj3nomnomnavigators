from django.shortcuts import render

# home view
def home(request):
    # include .html file extension 
    return render(request, 'home.html')

