from django.urls import path
# from . import views
	
# Create your views here. 

urlpatterns = [
	path('', views.home, name = 'home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
    path('accounts/signup/', views.signup, name='signup'),
]
