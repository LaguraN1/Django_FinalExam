from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from blog.models import Post, Comment
from blog.services.interaction_service import InteractionService

from .serializers import PostSerializer, CommentSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return Post.objects.published().select_related(
            "user"
        ).prefetch_related(
            "likes",
            "comments",
            "tags",
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.published().select_related(
            "user"
        ).prefetch_related(
            "likes",
            "comments",
            "tags",
        )

class PostLikeAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, slug):
        post = get_object_or_404(
            Post,
            slug=slug,
            is_published=True
        )

        created = InteractionService.like_post_idempotent(
            request.user,
            post
        )

        if created:
            message = "Post liked."
        else:
            message = "Post already liked."

        return Response(
            {
                "message": message,
                "liked": True,
                "likes_count": post.likes.count(),
            },
            status=status.HTTP_200_OK
        )
class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_post(self):
        return get_object_or_404(
            Post,
            slug=self.kwargs["slug"],
            is_published=True
        )

    def get_queryset(self):
        post = self.get_post()

        return Comment.objects.filter(
            post=post,
            parent__isnull=True
        ).select_related(
            "user"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        post = self.get_post()

        serializer.save(
            user=self.request.user,
            post=post
        )