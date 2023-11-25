from django.urls import path
from .views import PostDetailView,PostListView

urlpatterns = [
    path('', PostListView.as_view(),name="posts"),
    path('post/<slug:slug>/',PostDetailView.as_view(),name="post-detail"),
]
