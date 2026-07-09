from django.utils import timezone

from blog.models import Post


class PostService:

    @staticmethod
    def get_published_posts(query=None):
        posts = Post.objects.published().select_related(
            "user"
        ).prefetch_related(
            "tags"
        ).order_by("-created_at")

        if query:
            posts = posts.search(query)

        return posts

    @staticmethod
    def get_user_posts(user):
        return Post.objects.filter(
            user=user
        ).order_by("-created_at")

    @staticmethod
    def calculate_trending_score(post, gravity=1.8):
        age = timezone.now() - post.created_at
        age_hours = age.total_seconds() / 3600

        likes_count = post.likes.count()

        score = (likes_count - 1) / ((age_hours + 2) ** gravity)

        return score