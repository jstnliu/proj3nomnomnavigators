from django.urls import path
from . import views
	
# Create your views here. 

urlpatterns = [
    # 	RECIPE FUNCTIONS
	path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('recipes/', views.recipes_index, name = 'index'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name = 'detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name = 'recipes_create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name = 'recipes_update'),
    # 	DISH_TYPE FUNCTIONS
	path('dish_types/', views.Dish_TypeList.as_view(), name = 'dish_types_index'),
    path('dish_types/<int:pk>/', views.Dish_TypeDetail.as_view(), name = 'dish_types_detail'),
	path('dish_type/create/', views.Dish_TypeCreate.as_view(), name = 'dish_types_create'),
    path('dish_type/<int:pk>/update/', views.Dish_TypeUpdate.as_view(), name = 'dish_types_update'),
    # 	USER FUNCTIONS
    path('accounts/signup/', views.signup, name = 'signup'),
]
