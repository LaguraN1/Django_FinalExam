from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

from blog.models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    """ GET /api/posts/ and POST /api/posts/ """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the post author
        serializer.save(user=self.request.user)

class PostRetrieveAPIView(generics.RetrieveAPIView):
    """ GET /api/posts/<slug>/ """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class CommentListCreateAPIView(generics.ListCreateAPIView):
    """ GET /api/posts/<slug>/comments/ and POST /api/posts/<slug>/comments/ """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return Comment.objects.filter(post=post, parent=None) # Only return top-level comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        serializer.save(user=self.request.user, post=post)

class PostLikeAPIView(APIView):
    """ POST /api/posts/<slug>/like/ """
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like = Like.objects.filter(user=request.user, post=post)

        if like.exists():
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        else:
            Like.objects.create(user=request.user, post=post)
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)