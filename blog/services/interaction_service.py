from blog.models import Like, Bookmark, Follow


class InteractionService:

    @staticmethod
    def toggle_like(user, post):
        like, created = Like.objects.get_or_create(
            user=user,
            post=post
        )

        if not created:
            like.delete()
            return False

        return True

    @staticmethod
    def toggle_bookmark(user, post):
        bookmark, created = Bookmark.objects.get_or_create(
            user=user,
            post=post
        )

        if not created:
            bookmark.delete()
            return False

        return True

    @staticmethod
    def follow_user(follower, following):
        if follower == following:
            return False

        follow, created = Follow.objects.get_or_create(
            follower=follower,
            following=following
        )

        return created

    @staticmethod
    def unfollow_user(follower, following):
        deleted_count, _ = Follow.objects.filter(
            follower=follower,
            following=following
        ).delete()

        return deleted_count > 0