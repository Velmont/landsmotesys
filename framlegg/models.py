# vim: ts=4 sts=4 expandtab sw=4
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

class Document(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(Category)

    # Kinda-meta
    added = models.DateField()

    def __unicode__(self):
        return self.title

class Patch(models.Model):
    patch = models.TextField()
    document = models.ForeignKey(Document)
    written_by = models.CharField(max_length=200)

    # Info
    reason = models.TextField(blank=True, null=True)

    # Kinda-meta
    created = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
