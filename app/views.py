from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post
# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/all_posts.html'
    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post.html'