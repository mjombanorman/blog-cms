from django.urls import path
from .views import PostDetailView,PostListView,TagDetailView,AuthorDetailView



urlpatterns = [
    path('', PostListView.as_view(),name="posts"),
    path('post/<slug:slug>/',PostDetailView.as_view(),name="post-detail"),
    path('tag/<slug:slug>/', TagDetailView.as_view(), name="tag"),
    path('author/<slug:slug>/', AuthorDetailView.as_view(), name="author"),
]
