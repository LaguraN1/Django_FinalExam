from django.db import models
from django.db.models import Q


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(is_published=True)

    def drafts(self):
        return self.filter(is_published=False)

    def search(self, query):
        if not query:
            return self

        return self.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(user__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def drafts(self):
        return self.get_queryset().drafts()

    def search(self, query):
        return self.get_queryset().search(query)