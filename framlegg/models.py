# vim: ts=4 sts=4 expandtab sw=4
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    name = models.CharField(max_length=200)
    accepted = models.BooleanField()

    def __unicode__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(Category)

    # Voting
    nemnd_vote = models.ForeignKey(Vote, related_name="document_nemnd", null=True, blank=True)    # Innstilling
    final_vote = models.ForeignKey(Vote, related_name="document_final", null=True, blank=True)    # Vedtak

    # Kinda-meta
    created = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class Patch(models.Model):
    text = models.TextField()
    document = models.ForeignKey(Document)
    written_by = models.CharField(max_length=200)

    # Info
    reason = models.TextField(blank=True, null=True)

    # Voting
    nemnd_vote = models.ForeignKey(Vote, related_name="patch_nemnd", null=True, blank=True)    # Innstilling
    nemnd_superseeded_by = models.ForeignKey('Patch', null=True, blank=True)    # Innstilling
    final_vote = models.ForeignKey(Vote, related_name="patch_final", null=True, blank=True)    # Vedtak

    # Kinda-meta
    created = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=200)

    def __unicode__(self):
        return "Patch %d" % self.pk

