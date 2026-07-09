from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # GET /api/posts/ AND POST /api/posts/
    path('posts/', views.PostListCreateAPIView.as_view(), name='post-list'),
    
    # GET /api/posts/<slug>/
    path('posts/<slug:slug>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),
    
    # GET /api/posts/<slug>/comments/ AND POST /api/posts/<slug>/comments/
    path('posts/<slug:slug>/comments/', views.CommentListCreateAPIView.as_view(), name='post-comments'),
    
    # POST /api/posts/<slug>/like/
    path('posts/<slug:slug>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
]