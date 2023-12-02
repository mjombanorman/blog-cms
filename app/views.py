from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Post,Comments,Tag,Profile,WebsiteMeta
from django.shortcuts import get_object_or_404
from .forms import CommentForm,SubscribeForm,RegistrationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count


# Displaying of all posts in the blog
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/all_posts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if WebsiteMeta.objects.all().exists():
            context['meta'] = WebsiteMeta.objects.all().first()
        context['form'] = SubscribeForm()
        context["top_posts"] = self.model.objects.all().order_by(
            '-view_count')[:3]
        context["recent_posts"] = self.model.objects.all().order_by(
            '-last_update')[:3]
        context["featured_post"] = self.model.objects.filter(is_featured=True).first()
        return context

    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST)
        request.session['subscribed'] = True
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscribed successfully!')
        else:
            messages.error(request, 'Subscription failed. Please try again.')
        return redirect('posts')

        

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
        bookmarked = False
        if self.object.bookmarks.filter(id=self.request.user.id).exists():
            bookmarked = True                   
        is_liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            is_liked = True            
            
        context['is_bookmarked']=bookmarked
        context['is_liked'] = is_liked
        context['like_count'] = self.object.likes.all().count
        
        context["top_posts"] = self.model.objects.all().order_by(
            '-view_count')[:3]
        context["recent_posts"] = self.model.objects.all().order_by(
            '-last_update')[:2]
        
        context['top_authors'] = User.objects.annotate(number=Count('post')).order_by('-number')
        context['related_posts'] = self.model.objects.filter(author=self.object.author)[:2]
        context['tags']=Tag.objects.all()

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

class AboutView(ListView):
    model = WebsiteMeta
    context_object_name = 'meta'
    template_name = 'app/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if WebsiteMeta.objects.all().exists():
            context['meta'] = WebsiteMeta.objects.all().first()
      
        return context

class TagDetailView(DetailView):
    model = Tag
    template_name = "app/tag.html"
    context_object_name = 'tag'
    
       # get the post based on the slug

    def get_object(self, queryset=None):
        # allow updating of view count in returned post
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubscribeForm()
        #filter top posts using tags id
        context['tags'] = self.model.objects.all()
        context["top_posts"] = Post.objects.filter(tags__in=self.model.objects.filter(slug=self.kwargs['slug'])).order_by(
            '-view_count')[:3]
        context["recent_posts"] = Post.objects.filter(
            tags__in=self.model.objects.filter(slug=self.kwargs['slug'])).order_by('-last_update')[:3]
        return context


class AuthorDetailView(DetailView):
    model = Profile
    template_name = "app/author.html"
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubscribeForm()
        author = get_object_or_404(
            Profile, slug=self.kwargs['slug'])
        # filter top posts using tags id
        context['author'] = author
        context["top_posts"] = Post.objects.filter(author=author.user).order_by('-view_count')[:2]
        context["recent_posts"] = Post.objects.filter(author=author.user).order_by('-last_update')[:3]
        context["top_authors"] = User.objects.annotate(number=Count('post')).order_by('-number')[:3]
        return context


# Searchview to allow user search data in the blog
class SearchView(ListView):
    template_name = 'app/search.html'
    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            posts = Post.objects.filter(title__icontains=query)
            print(posts)
        else:
            posts = Post.objects.none()  # Return an empty queryset if there's no query
            print(posts)
        return posts


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'registration/signup.html'
    success_url = "/accounts/login/"  # Assuming 'posts' is the URL name for your posts view
    success_message = "Your account was registered successfully"
    form_class = RegistrationForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


def BookmarkPost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
        messages.info(request, 'You have removed this post from the bookmark.')
    else:
        post.bookmarks.add(request.user)
        messages.info(request, 'You have bookmarked this post.')
    return redirect('post-detail', slug)


def LikePost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
  
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.info(request, 'You have unliked the post.')
    else:
        post.likes.add(request.user)
        messages.info(request, 'You have liked this post.')
    return redirect('post-detail', slug)



class MyBookmarksView(ListView):
    model = Post
    context_object_name = 'bookmarked_posts'
    template_name = 'app/my_bookmarks.html'
      
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(bookmarks=self.request.user.id)
    
    
class MyLikesView(ListView):
    model = Post
    context_object_name = 'liked_posts'
    template_name = 'app/my_likes.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(likes=self.request.user.id)


   
class MyPostsView(ListView):
    model = Post
    context_object_name = 'my_posts'
    template_name = 'app/my_posts.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(author=self.request.user)
