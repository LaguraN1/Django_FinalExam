from rest_framework import serializers

from blog.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source="user.username",
        read_only=True
    )

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    comments_count = serializers.IntegerField(
        source="comments.count",
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "slug",
            "body",
            "is_published",
            "views",
            "likes_count",
            "comments_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "slug",
            "views",
            "likes_count",
            "comments_count",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "body",
            "parent",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "created_at",
        ]