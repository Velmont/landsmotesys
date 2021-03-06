# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
# Copyright 2009, 2010 Nei til EU, Odin Hørthe Omdal
#
# This file is part of Landsmotesys.
#
# Landsmotesys is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Landsmotesys is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Landsmotesys.  If not, see <http://www.gnu.org/licenses/>.
from django.db import models
from django.forms import ModelForm, ValidationError
from django.db.models import permalink
import datetime
import textwrap

class Category(models.Model):
    name = models.CharField("saknamn", max_length=200)
    time_limit = models.DateTimeField("innleveringsfrist")

    class Meta:
        ordering = ('name',)
        verbose_name = "Sak"
        verbose_name_plural = "Saker"

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
    ('NA', 'Inga tilråding teke'),
)

VOTE_CHOICES = (
    ('W', 'Ikkje stemt over'),
    ('A', 'Tilrådd vedteke'),
    ('D', 'Tilrådd avvist'),
)

class Document(models.Model):
    title = models.CharField("tittel", max_length=200)
    text = models.TextField("tekst", null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="sak")
    backed_by = models.CharField("fremja av", max_length=200)

    # Voting
    nemnd_accepted = models.CharField("innstilling", max_length=2,
                                      choices=VOTE_NEMND_CHOICES,
                                      default="W")
    nemnd_desc = models.TextField("nemnd kvifor?", blank=True, null=True,
                                help_text="""Fritekst til spesielle kommentarar""")
    accepted = models.CharField("vedtak", max_length=2,
                                choices=VOTE_CHOICES,
                                default="W")

    # Kinda-meta
    created = models.DateTimeField("opretta", default=datetime.datetime.now)
    created_by = models.CharField("oppretta av", max_length=200, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = "Dokument"
        verbose_name_plural = "Dokument"

    def num_patches(self):
        return self.patch_set.all().count()
    num_patches.short_description = "framlegg"

    def num_undef_patches(self):
        return self.patch_set.filter(nemnd_accepted='W').count()
    num_undef_patches.short_description = "nye"

    def num_undef_patches_color(self):
        c = self.num_undef_patches()
        if c == 0:
            return "-"

        return "<strong style='color:red'>%d</strong>" % c
    num_undef_patches_color.short_description = "nye"
    num_undef_patches_color.allow_tags = True

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Wrap dersom det er fyrste gong me lagrar dokumentet
        if not self.id:
            self.text = textwrap.fill(self.text, width=78, replace_whitespace=False)
        super(Document, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('framlegg.views.document', [str(self.pk)])

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'text', 'backed_by')

    def clean(self):
        """Set category hardkoda til primary key 1 (fråsegner/uttalelser)"""
        cat = Category.objects.get(pk=1)
        self.instance.category = cat
        if cat.time_limit < datetime.datetime.now():
            raise ValidationError("Tidsfristen er ute!")

        return self.cleaned_data


class Patch(models.Model):
    document = models.ForeignKey(Document, verbose_name="dokument")
    backed_by = models.CharField("fremja av", max_length=200, help_text="""
<p class="forklaring">Namnet ditt (og eventuelt andre), separert med komma""")
    line_no = models.CharField("linenr (eller post)", max_length=20, help_text="""
<p class="forklaring">Start med eit tal, t.d. <code>123-125,145</code>.
Viss sak er budsjett skriv du inn relevant post.</p>""")

    what_to_change = models.TextField("endring", help_text="""<div class="forklaring">
<p>Dersom det er ei endring du kjem med, skriv det på følgjande måte:</p>
         <pre>Endra line 123-125 frå:

> Nei til EU skal i dei komande vekene gjera mykje bra.

til:

> Nei til EU skal i dei komande vekene gjera heilt ekstremt mykje bra.</pre></div>""")
    diff = models.TextField(blank=True, null=True)

    # Info
    reason = models.TextField("grunngjeving", blank=True, null=True, help_text="""
<p class="forklaring">Friviljugt felt</p>""")

    # Voting
    nemnd_accepted = models.CharField("innstilling", max_length=2,
        choices=VOTE_NEMND_CHOICES,
        default="W")
    accepted = models.CharField("vedtak", max_length=2,
       choices=VOTE_CHOICES,
       default="W")
    nemnd_desc = models.TextField("nemnd kvifor?", blank=True, null=True,
                                help_text="""Fritekst til spesielle kommentarar""")
    nemnd_superseeding = models.ForeignKey('self', verbose_name='fyretrekt framfor',
                                            help_text="""Framlegget du veljer her vert plassert
                                              oppfor og som «forelder» til dette framlegget""",
                                            related_name='nemnd_superseeded_by',
                                            null=True, blank=True)

    # Kinda-meta
    created = models.DateTimeField("oppretta", default=datetime.datetime.now)
    created_by = models.CharField("oppretta av", max_length=200, blank=True)

    class Meta:
        verbose_name = "Framlegg"
        verbose_name_plural = "Framlegg"

    def __unicode__(self):
        if self.id:
            return "Framlegg %d" % self.id
        return "Framlegg <ukjend>"

class PatchForm(ModelForm):
    class Meta:
        model = Patch
        fields = ('backed_by', 'line_no', 'what_to_change', 'reason')

    def clean(self):
        doc = self.instance.document
        if doc.category.time_limit < datetime.datetime.now():
            raise ValidationError("Tidsfristen er ute!")
        return self.cleaned_data

