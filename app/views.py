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
    
    # Getting Top Posts and Recent Posts into the context dictionary
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_posts"] = self.model.objects.all().order_by('-view_count')[:3]
        context["recent_posts"] = self.model.objects.all().order_by('-last_update')[:3]
        return context



# Displaying a single blog post
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post.html'
    
    # get the post based on the slug
    def get_object(self, queryset=None):
        #allow updating of view count in returned post
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        
        # when view_count is None initialize with 0
        if post.view_count is None:
            post.view_count = 0
        post.view_count = post.view_count + 1
        post.save()
        return post
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add an instance of only comments and form excluding the reply
        context['comments'] = Comments.objects.filter(
            post=self.object, parent=None)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        form = CommentForm(request.POST)

        if form.is_valid():
            
            # checking if the post request sent contains a reply then save to database as a reply
            if request.POST.get('parent'):
                parent = Comments.objects.get(id=request.POST.get('parent'))
                comment_reply = form.save(commit=False)
                comment_reply.parent = parent
                comment_reply.post = post
                comment_reply.save()
                return redirect('post-detail', self.kwargs['slug'])
            
            # Process the form data and save the comment
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
       
        # Redirect to the same page with updated context
        return redirect('post-detail', self.kwargs['slug'])

