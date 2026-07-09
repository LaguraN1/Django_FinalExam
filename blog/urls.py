from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),

    path(
        "tag/<slug:slug>/",
        views.TagPostsView.as_view(),
        name="tag-posts"
    ),

    path(
        "trending/",
        views.TrendingPostsView.as_view(),
        name="trending-posts"
    ),

    path("post/create/", views.PostCreateView.as_view(), name="post-create"),

    path(
        "post/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post-detail"
    ),

    path(
        "post/<slug:slug>/edit/",
        views.PostUpdateView.as_view(),
        name="post-update"
    ),

    path(
        "post/<slug:slug>/delete/",
        views.PostDeleteView.as_view(),
        name="post-delete"
    ),

    path(
        "post/<slug:slug>/comment/",
        views.CommentCreateView.as_view(),
        name="comment-create"
    ),

    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete"
    ),

    path(
        "comment/<int:comment_id>/reply/",
        views.reply_comment,
        name="comment-reply"
    ),

    path(
        "post/<slug:slug>/like/",
        views.like_post,
        name="like-post"
    ),

    path(
        "post/<slug:slug>/bookmark/",
        views.bookmark_post,
        name="bookmark-post"
    ),

    path(
        "profile/<str:username>/",
        views.ProfileView.as_view(),
        name="profile"
    ),

    path(
        "profile/<str:username>/follow/",
        views.follow_user,
        name="follow"
    ),

    path(
        "profile/<str:username>/unfollow/",
        views.unfollow_user,
        name="unfollow"
    ),

    path(
        "bookmarks/",
        views.MyBookmarksView.as_view(),
        name="bookmarks"
    ),
]