# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
from django.db import models
from django.forms import ModelForm

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

    class Meta:
        ordering = ('category', '-created')

    def num_patches(self):
        return self.patch_set.all().count()

    def __unicode__(self):
        return self.title


class Patch(models.Model):
    document = models.ForeignKey(Document)
    backed_by = models.CharField("Foreslått av", max_length=200, help_text="""
<p class="forklaring">Namnet ditt (og eventuelt andre)""")
    line_no = models.CharField("Linenummer", max_length=20, help_text="""
<p class="forklaring">Start med eit tal, t.d. <code>123-125,145</code></p>""")

    what_to_change = models.TextField("Endringsframlegg", help_text="""<div class="forklaring">
<p>Dersom det er ei endring du kjem med, skriv det på følgjande måte:</p>
         <pre>Endra line 123-125 frå:

> Nei til EU skal i dei komande vekene gjera mykje bra.

til:

> Nei til EU skal i dei komande vekene gjera heilt ekstremt mykje bra.</pre></div>"""
)
    diff = models.TextField(blank=True, null=True)

    # Info
    reason = models.TextField(blank=True, null=True)

    # Voting
    nemnd_accepted = models.BooleanField(default=False)
    nemnd_desc = models.TextField(blank=True, null=True)
    nemnd_superseeded_by = models.ForeignKey('Patch', null=True, blank=True)
    accepted = models.BooleanField(default=False) # Vedtak

    # Kinda-meta
    created = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=200)

    def __unicode__(self):
        return "Patch %d" % self.pk

class PatchForm(ModelForm):
    class Meta:
        model = Patch
        fields = ('backed_by', 'line_no', 'what_to_change')
