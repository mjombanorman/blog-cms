from typing import Any
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import CommentForm



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
    
    
    #Getting post based on the slug
    def get_object(self, queryset=None):
        # Retrieve the object based on the slug or any other unique identifier
        obj = get_object_or_404(Post, slug=self.kwargs['slug'])
        # Update the view_count here
        obj.view_count = obj.view_count + 1 if obj.view_count is not None else 1
        obj.save()

        return obj
    
    # Adding the model form as a context variable
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add an instance of CommentForm to the context
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            # Process the form data and save the comment
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # Redirect or do something after successful comment submission

        # If the form is invalid or after processing, render the same page with updated context
        return self.render_to_response(self.get_context_data(form=form))

    