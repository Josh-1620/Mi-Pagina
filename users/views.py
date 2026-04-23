
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from movies.models import MovieReview, MovieLike
from django.contrib.auth.decorators import login_required
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request,'users/profile.html')
    


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))
        else:
            # Return an 'invalid login' error message.
            return render(request, 'users/login.html', {'errors':['Invalid Login']})
    else:
        return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request):
    
    user_reviews = MovieReview.objects.filter(user=request.user).select_related('movie')
    user_likes = MovieLike.objects.filter(user=request.user).select_related('movie')
    
    context = {
        'reviews': user_reviews,
        'likes': user_likes,
    }
    return render(request, 'users/profile.html', context)