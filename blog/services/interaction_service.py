from django.db import IntegrityError, transaction

from blog.models import Like, Bookmark, Follow


class InteractionService:

    @staticmethod
    def like_post_idempotent(user, post):
        """
        Creates a like only once.
        If the like already exists, it does not create duplicate likes.
        """

        try:
            with transaction.atomic():
                like, created = Like.objects.get_or_create(
                    user=user,
                    post=post
                )

                return created

        except IntegrityError:
            return False

    @staticmethod
    def bookmark_post_idempotent(user, post):
        """
        Creates a bookmark only once.
        If the bookmark already exists, it does not create duplicates.
        """

        try:
            with transaction.atomic():
                bookmark, created = Bookmark.objects.get_or_create(
                    user=user,
                    post=post
                )

                return created

        except IntegrityError:
            return False

    @staticmethod
    def follow_user(follower, following):
        """
        Follows a user only once.
        Prevents duplicate follow records.
        """

        if follower == following:
            return False

        try:
            with transaction.atomic():
                follow, created = Follow.objects.get_or_create(
                    follower=follower,
                    following=following
                )

                return created

        except IntegrityError:
            return False

    @staticmethod
    def toggle_like(user, post):
        """
        Used for website button:
        like if not liked, unlike if already liked.
        """

        like = Like.objects.filter(
            user=user,
            post=post
        )

        if like.exists():
            like.delete()
            return False

        InteractionService.like_post_idempotent(
            user,
            post
        )

        return True

    @staticmethod
    def toggle_bookmark(user, post):
        """
        Used for website button:
        save if not saved, remove if already saved.
        """

        bookmark = Bookmark.objects.filter(
            user=user,
            post=post
        )

        if bookmark.exists():
            bookmark.delete()
            return False

        InteractionService.bookmark_post_idempotent(
            user,
            post
        )

        return True

    @staticmethod
    def unfollow_user(follower, following):
        deleted_count, deleted_data = Follow.objects.filter(
            follower=follower,
            following=following
        ).delete()

        return deleted_count > 0