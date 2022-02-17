from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['authors', 'header', 'text', 'rating_post', 'paper_news',]
