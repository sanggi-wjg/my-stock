from django.db import models

from mystock.core.constants import ALLOW_INDEXES


class IndexQuerySet(models.QuerySet):
    def initialize_indexes(self):
        for index_name in ALLOW_INDEXES:
            self.get_or_create(name=index_name)

    def is_exists_index(self, index_name: str):
        return self.filter(name=index_name).exists()


class Index(models.Model):
    objects = IndexQuerySet.as_manager()

    class Meta:
        db_table = "index"

    name = models.CharField(max_length=254, unique=True)
