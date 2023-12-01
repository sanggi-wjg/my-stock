from django.db import models

from mystock.core.constants import ALLOW_INDEXES


class IndexQuerySet(models.QuerySet):
    def initialize_markets(self):
        for index_name in ALLOW_INDEXES:
            self.get_or_create(name=index_name)


class Index(models.Model):
    objects = IndexQuerySet.as_manager()

    class Meta:
        db_table = "index"

    name = models.CharField(max_length=254, unique=True)
