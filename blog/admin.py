from django.contrib import admin
from .models import Post, Tag, Comment, Like, Bookmark, Follow


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = [
        "user",
        "body",
        "parent",
        "created_at",
    ]
    readonly_fields = [
        "created_at",
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "is_published",
        "views",
        "created_at",
    ]

    search_fields = [
        "title",
        "body",
        "user__username",
        "tags__name",
    ]

    list_filter = [
        "is_published",
        "created_at",
        "updated_at",
        "tags",
    ]

    prepopulated_fields = {
        "slug": ["title"],
    }

    inlines = [
        CommentInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]

    search_fields = [
        "name",
        "slug",
    ]

    prepopulated_fields = {
        "slug": ["name"],
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "post",
        "parent",
        "created_at",
    ]

    search_fields = [
        "body",
        "user__username",
        "post__title",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "post",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "post__title",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "post",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "post__title",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        "follower",
        "following",
        "created_at",
    ]

    search_fields = [
        "follower__username",
        "following__username",
    ]

    list_filter = [
        "created_at",
    ]