from django.urls import path
from .views import *

app_name = 'movies'

urlpatterns = [
    path('', index, name='index'),
    
    path('all/', all_movies, name='all_movies'),
    path('saludo/<int:veces>/', saludo, name='saludo'),

    path('<int:movie_id>/', movie, name='movie_detail'),

    path('movie_like/add/<int:movie_id>/', add_like, name='toggle_like'),
    path('movie_review/add/<int:movie_id>/', add_review, name='add_review'),
    path('movie_reviews/<int:movie_id>/', movie_reviews, name='movie_reviews'),
    
]