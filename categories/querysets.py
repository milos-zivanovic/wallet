from django.conf import settings
from django.db import models
from django.db.models import F, Q, Exists, OuterRef, Func, Value, DateField
from django.utils.timezone import now


class CategoryGroupQuerySet(models.QuerySet):

    def active(self, check_date=None):
        check_date = check_date or now().date()

        from .models import Category
        active_categories = Category.objects.active(check_date)

        return self.filter(
            Exists(
                active_categories.filter(category_group=OuterRef('pk'))
            )
        )


class CategoryQuerySet(models.QuerySet):

    def active(self, check_date=None):
        check_date = check_date or now().date()
        current_year = check_date.year

        qs = self.filter(
            Q(start_date__lte=check_date) | Q(start_date__isnull=True),
            Q(end_date__gte=check_date) | Q(end_date__isnull=True)
        )

        if not settings.DEBUG:
            # Production: annotate with MAKE_DATE for periodic month/day
            qs = qs.annotate(
                periodic_start_date=Func(
                    Value(current_year), F('start_month'), F('start_day'),
                    function='MAKE_DATE', output_field=DateField()
                ),
                periodic_end_date=Func(
                    Value(current_year), F('end_month'), F('end_day'),
                    function='MAKE_DATE', output_field=DateField()
                )
            ).filter(
                Q(periodic_start_date__lte=check_date) |
                Q(start_month__isnull=True) | Q(start_day__isnull=True),
                Q(periodic_end_date__gte=check_date) |
                Q(end_month__isnull=True) | Q(end_day__isnull=True)
            )

        return qs
