from django.urls import path
from .views import PostDetailView,PostListView,TagDetailView,AuthorDetailView,AboutView,SearchView,RegisterUserView,BookmarkPostView


urlpatterns = [
    path('', PostListView.as_view(),name="posts"),
    path('post/<slug:slug>/',PostDetailView.as_view(),name="post-detail"),
    path('tag/<slug:slug>/', TagDetailView.as_view(), name="tag"),
    path('author/<slug:slug>/', AuthorDetailView.as_view(), name="author"),
    path('search/', SearchView.as_view(), name="search"),
    path('about/', AboutView.as_view(), name="about"),
    path('accounts/register/', RegisterUserView.as_view(), name="register"),
    path('bookmark-post/<slug:slug>', BookmarkPostView, name="bookmark"),
]
