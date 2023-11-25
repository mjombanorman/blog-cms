from typing import Any
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post
from django.shortcuts import get_object_or_404
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/all_posts.html'
    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post.html'
    
    def get_object(self, queryset=None):
        # Retrieve the object based on the slug or any other unique identifier
        obj = get_object_or_404(Post, slug=self.kwargs['slug'])
        
        # Update the view_count here
        obj.view_count = obj.view_count + 1 if obj.view_count is not None else 1
        obj.save()
        
        return obj
    
    # def get_queryset(self,**kwargs):
    #     queryset = Post.objects.filter(slug=self.kwargs['slug'])
    #     if queryset.view_count is None:
    #         queryset.view_count = 1
    #     else:
    #         queryset.view_count = queryset.view_count + 1
    #     queryset.save()
    #     return queryset
    

        

    