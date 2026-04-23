from django import forms


class MovieCommentForm(forms.Form):
    review = forms.CharField(label="Reseña", min_length=5, required=True, 
                             widget =  forms.Textarea(attrs={"class": "block w-full rounded-md bg-white px-3" 
                                  "py-1.5 text-base text-gray-900 outline outline-1"
                                  "-outline-offset-1 outline-gray-300 placeholder:text-gray-400" 
                                  "focus:outline focus:outline-2 focus:-outline-offset-2" 
                                  "focus:outline-indigo-600 sm:text-sm/6"}) ) 

from django import forms
from .models import MovieReview

class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['title', 'rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de tu reseña'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }