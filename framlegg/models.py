# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
from django.db import models
from django.forms import ModelForm
from django.db.models import permalink
import datetime

class Category(models.Model):
    name = models.CharField(max_length=200)

    @models.permalink
    def get_absolute_url(self):
        return ('framlegg.views.cat_view', [str(self.pk)])

    def __unicode__(self):
        return self.name

# Proposed accepted/declined
VOTE_NEMND_CHOICES = (
    ('W', 'Inga tilråding enno'),
    ('PA', 'Tilrådd vedteke'),
    ('PD', 'Tilrådd avvist'),
)

VOTE_CHOICES = (
    ('W', 'Ingen stemme'),
    ('A', 'Tilrådd vedteke'),
    ('D', 'Tilrådd avvist'),
)

class Document(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category)

    # Voting
    nemnd_accepted = models.CharField(max_length=2,
                                      choices=VOTE_NEMND_CHOICES,
                                      default="W")
    accepted = models.CharField(max_length=2,
                                choices=VOTE_CHOICES,
                                default="W")

    # Kinda-meta
    created = models.DateField(default=datetime.date.today)
    created_by = models.CharField(max_length=200)

    class Meta:
        ordering = ('category', '-created')

    def num_patches(self):
        return self.patch_set.all().count()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('framlegg.views.document', [str(self.pk)])

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('category', 'title', 'text', 'created_by')


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
    reason = models.TextField("Grunngjeving", blank=True, null=True, help_text="""
<p class="forklaring">Friviljugt felt</p>""")

    # Voting
    nemnd_accepted = models.CharField(max_length=2,
        choices=VOTE_NEMND_CHOICES,
        default="W")
    accepted = models.CharField(max_length=2,
       choices=VOTE_CHOICES,
       default="W")
    nemnd_desc = models.TextField(blank=True, null=True)
    nemnd_superseeded_by = models.ForeignKey('Patch', null=True, blank=True)

    # Kinda-meta
    created = models.DateField(default=datetime.date.today)
    created_by = models.CharField(max_length=200, default="Systemet")

    def __unicode__(self):
        return "Patch %d" % self.pk

class PatchForm(ModelForm):
    class Meta:
        model = Patch
        fields = ('backed_by', 'line_no', 'what_to_change', 'reason')
