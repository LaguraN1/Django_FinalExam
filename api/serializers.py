from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Tag

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'avatar_url']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at', 'parent']
        read_only_fields = ['user', 'post', 'parent']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'slug', 'body', 'is_published', 'views', 'tags', 'created_at']
        read_only_fields = ['views', 'slug', 'user']