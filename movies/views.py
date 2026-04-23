from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieReview, Person, MovieLike
from movies.forms import MovieReviewForm, MovieCommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .utils import fetch_from_tmdb


def all_movies(request):
    movies = Movie.objects.all() # Movies de la BD
    context = { 'objetos':movies, 'message':'welcome' }
    return render(request,'movies/allmovies.html', context=context )

def index(request):
   
    data = fetch_from_tmdb("movie/now_playing")
    movies_api = data.get('results', []) if data else []
    
    context = {
        'movies': movies_api,
        'message': 'Películas más recientes'
    }
    return render(request, 'movies/index.html', context)

def saludo(request, veces):
    saludo = 'Hola ' * veces
    personas = Person.objects.all()
    context = { 'saludo':saludo, 'lista':personas }
    return render(request,'movies/saludo.html', context=context )

def movie(request, movie_id):
   
    movie_data = fetch_from_tmdb(f"movie/{movie_id}", params={'append_to_response': 'credits'})
    
    if not movie_data:
        return HttpResponse(f"Error: No se pudo obtener la película {movie_id}", status=404) 

    
    reviews = MovieReview.objects.filter(movie__tmdb_id=movie_id).order_by('-created_at')
    
    
    user_likes_this = False
    if request.user.is_authenticated:
        user_likes_this = MovieLike.objects.filter(user=request.user, movie__tmdb_id=movie_id).exists()

    context = {
        'movie': movie_data,
        'actors': movie_data.get('credits', {}).get('cast', [])[:10],
        'reviews': reviews,
        'review_form': MovieReviewForm(),
        'user_likes_this': user_likes_this, 
    }
    return render(request, 'movies/movie.html', context)


def movie_reviews(request, movie_id):
    # Filtramos por el tmdb_id de la película
    reviews = MovieReview.objects.filter(movie__tmdb_id=movie_id).order_by('-created_at')
    return render(request, 'movies/reviews.html', {'reviews': reviews})

@login_required
def user_collections(request):
   
    likes = MovieLike.objects.filter(user=request.user).select_related('movie')
    return render(request, 'movies/collections.html', {'likes': likes})




@login_required
def add_like(request, movie_id):
  
    movie_local, created = Movie.objects.get_or_create(
        tmdb_id=movie_id, 
        defaults={'title': 'Cargando...'}
    )
    
    if created:
        data = fetch_from_tmdb(f"movie/{movie_id}")
        if data:
            movie_local.title = data.get('title')
            movie_local.poster_path = data.get('poster_path')
            movie_local.save()

   
    like, created_like = MovieLike.objects.get_or_create(user=request.user, movie=movie_local)
    
    if not created_like:
        like.delete()
        return HttpResponse("🤍 Like") 
    
    return HttpResponse("❤️ Ya te gusta")



@login_required # Evita que usuarios no logueados entren
def add_review(request, movie_id):
    movie, created = Movie.objects.get_or_create(tmdb_id=movie_id, defaults={'title': 'Temporal'})
    
    if created:
        data = fetch_from_tmdb(f"movie/{movie_id}")
        if data:
            movie.title = data.get('title', 'Sin título')
            movie.overview = data.get('overview', '')
            movie.poster_path = data.get('poster_path', '')
            r_date = data.get('release_date')
            movie.release_date = r_date if r_date else None
            movie.running_time = data.get('runtime', 0)
            movie.save()

    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            
            return HttpResponse(status=204, headers={'HX-Trigger': 'listChanged'})
    else:
        form = MovieReviewForm()
        
    return render(request, 'movies/movie_review_form.html', {
        'movie_review_form': form, 
        'movie': movie
    })