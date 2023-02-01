from django import forms
from .models import Reviews

class CommentForm(forms.ModelForm):

    class Meta:
        models = Reviews
        fields = ['review',]
