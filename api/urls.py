from django.urls import path

from . import views


app_name = "api"


urlpatterns = [
    path(
        "posts/",
        views.PostListCreateAPIView.as_view(),
        name="post-list-create"
    ),

    path(
        "posts/<slug:slug>/",
        views.PostDetailAPIView.as_view(),
        name="post-detail"
    ),

    path(
        "posts/<slug:slug>/like/",
        views.PostLikeAPIView.as_view(),
        name="post-like"
    ),

    path(
        "posts/<slug:slug>/comments/",
        views.PostCommentListCreateAPIView.as_view(),
        name="post-comments"
    ),
]