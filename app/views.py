from typing import Any
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post,Comments
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.shortcuts import redirect


# Displaying of all posts in the blog
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/all_posts.html'


# Displaying a single blog post
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post.html'
    
    # get the post based on the slug
    def get_object(self, queryset=None):
        #allow updating of view count in returned post
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        post.view_count += 1
        post.save()
        return post
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add an instance of CommentForm to the context
        context['comments'] = Comments.objects.filter(post=self.object)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        form = CommentForm(request.POST)

        if form.is_valid():
            # Process the form data and save the comment
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
       
        # Redirect or do something after successful comment submission
        # If the form is invalid or after processing, render the same page with updated context
        return redirect('post-detail', self.kwargs['slug'])

