from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieReview, Person, MovieLike
from movies.forms import MovieReviewForm, MovieCommentForm
from django.http import HttpResponse
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
        # En lugar de buscar un template que no existe, lanzamos un texto simple
        return HttpResponse(f"Error: No se pudo obtener la película {movie_id} de TMDB. Revisa tu API Key.", status=404) 

    # El resto del código se queda igual...
    reviews = MovieReview.objects.filter(movie__tmdb_id=movie_id).order_by('-created_at')
    review_form = MovieReviewForm()
    
    context = {
        'movie': movie_data,
        'actors': movie_data.get('credits', {}).get('cast', [])[:10],
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'movies/movie.html', context)


def movie_reviews(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request,'movies/reviews.html', context={'movie':movie } )

def add_like(request, movie_id):
    form = None
    movie = Movie.objects.get(id=movie_id)

    if request.method == 'POST':
        form = MovieCommentForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['review']
            movie_like = MovieLike(
                    movie=movie,
                    review=review,
                    user=request.user)
            movie_like.save()
            return HttpResponseRedirect('/movies/')
    else:
        form = MovieCommentForm()
        return render(request,
                  'movies/movie_comment_form.html',
                  {'form': form, 'movie':movie})

def add_review(request, movie_id):
  
    movie, created = Movie.objects.get_or_create(tmdb_id=movie_id, defaults={'title': 'Cargando...'})
    
    if created:
        data = fetch_from_tmdb(f"movie/{movie_id}")
        if data:
            movie.title = data.get('title', 'Sin título')
            movie.overview = data.get('overview', '')
            movie.poster_path = data.get('poster_path', '')
            
            movie.release_date = data.get('release_date') if data.get('release_date') else None
            movie.running_time = data.get('runtime', 0)
            movie.save()

    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            
            rating = form.cleaned_data['rating']
            title  = form.cleaned_data['title']
            review = form.cleaned_data['review']
            
            
            movie_review = MovieReview(
                movie=movie,
                rating=rating,
                title=title,
                review=review,
                user=request.user
            )
            movie_review.save()
            
            
            return HttpResponse(status=204, headers={'HX-Trigger': 'listChanged'})
    else:
        form = MovieReviewForm()
        
    return render(request, 'movies/movie_review_form.html', {
        'movie_review_form': form, 
        'movie': movie
    })
