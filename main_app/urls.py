from django.urls import path
from . import views
	
# Create your views here. 

urlpatterns = [
    # 	RECIPE FUNCTIONS
	path('', views.home, name = 'home'),
    path('recipes/', views.recipes_index, name = 'index'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name = 'detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name = 'recipes_create'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name = 'recipes_delete'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name = 'recipes_update'),
    path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'),
    # 	DISH_TYPE FUNCTIONS
	path('dish_types/', views.Dish_TypeList.as_view(), name = 'dish_types_index'),
    path('dish_types/<int:pk>/', views.Dish_TypeDetail.as_view(), name = 'dish_types_detail'),
	path('dish_types/create/', views.Dish_TypeCreate.as_view(), name = 'dish_types_create'),
    path('dish_types/<int:pk>/delete/', views.Dish_TypeDelete.as_view(), name = 'dish_types_delete'),
    path('dish_types/<int:pk>/update/', views.Dish_TypeUpdate.as_view(), name = 'dish_types_update'),
    #   PHOTO FUNCTIONS
  	path('recipes/<int:recipe_id>/add_photo/', views.add_photo, name = 'add_photo'),
    # 	USER FUNCTIONS
    path('accounts/signup/', views.signup, name = 'signup'),

]
