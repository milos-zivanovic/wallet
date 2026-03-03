from django.db import models
from .querysets import CategoryGroupQuerySet, CategoryQuerySet


class ActiveCategoryGroupManager(models.Manager.from_queryset(CategoryGroupQuerySet)):

    def get_queryset(self):
        return super().get_queryset().active()


class ActiveCategoryManager(models.Manager.from_queryset(CategoryQuerySet)):

    def get_queryset(self):
        return super().get_queryset().active()
