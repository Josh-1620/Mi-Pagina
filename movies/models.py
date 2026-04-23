from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=80)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True) 
    profile_path = models.CharField(max_length=255, null=True, blank=True) 
    def __str__(self):
        return self.name
    
class Person(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=80)
    overview = models.TextField()
    release_date = models.DateField(null=True, blank=True) 
    running_time = models.IntegerField(null=True, blank=True)
    budget = models.BigIntegerField(blank=True, null=True) 
    tmdb_id = models.IntegerField(unique=True) #cambio para referenciar la API
    
    revenue = models.IntegerField(blank=True, null=True)
    poster_path = models.URLField(blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Person, through='MovieCredit')

    def __str__(self):
        return f'{self.title} ({self.release_date.year if self.release_date else "N/A"})'


class MovieCredit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    character = models.CharField(max_length=255, blank=True, null=True) # Personaje


class MovieLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   

class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    review = models.TextField(blank=True)
    title = models.TextField(blank=False, null=False, default="Reseña")
    created_at = models.DateTimeField(auto_now_add=True) #para saber cuando se voto

