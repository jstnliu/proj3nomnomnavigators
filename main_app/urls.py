from django.urls import path
from . import views
	
# Create your views here. 

urlpatterns = [
	path('', views.home, name = 'home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
]
