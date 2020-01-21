import datetime

from django.db import models
from django.utils import timezone

#datetime e timezone utili nel caso di funzioni sulle date
# come da tutorial

LANGUAGES = (
    ('it', 'Italiano'),
    ('en', 'English'),
    ('slo', 'Slovenski jezik'),
    ('de', 'Deutsche sprache'),
    ('hrv', 'Hrvatski jezik'),
)


class Category(models.Model):
    key = models.CharField(max_length=2)
    name = models.CharField(max_length=256)
    emoji = models.CharField(max_length=9, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="descrizione")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categorie"

    def __str__(self):
        return "Category " + str(self.key) + ' (' + \
               str(self.name) + ') ' + str(self.emoji)


class FileItem(models.Model):
    file_field = models.FileField(upload_to='uploads/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return "" + str(self.id) + " : " + self.file_field.name + "" + self.upload_date.strftime(
            "%d/%m/%y")


class Area(models.Model):
    area_name = models.CharField(max_length=1024, verbose_name="nome dell'area")

    where = models.TextField(max_length=1024, blank=True, null=True, verbose_name="dove?")
    when = models.TextField(max_length=1024, blank=True, null=True, verbose_name="quando?")
    how = models.TextField(max_length=1024, blank=True, null=True, verbose_name="come?")
    for_who = models.TextField(max_length=1024, blank=True, null=True, verbose_name="per chi?")

    image = models.ForeignKey(FileItem, on_delete=models.PROTECT, null=True, blank=True, verbose_name="immagine")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data inserimento')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Aree'

    def __str__(self):
        return self.area_name


class Content(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    title = models.CharField(max_length=1024)
    text = models.TextField(max_length=4096, blank=True, null=True,)

    image = models.ForeignKey(FileItem, on_delete=models.PROTECT, null=True, blank=True, verbose_name="immagine")

    categories = models.ManyToManyField(Category, blank=True, verbose_name="categorie")

    link = models.CharField(max_length=1024, blank=True, null=True)
    link_caption = models.CharField(max_length=1024, blank=True, null=True, default="continua")

    lang = models.CharField(max_length=3, choices=LANGUAGES, default='it',
                            verbose_name="lingua")

    linked_contents = models.ManyToManyField('Content', blank=True, verbose_name="contenuti collegati")

    level = models.SmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data inserimento')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contenuto'
        verbose_name_plural = 'Contenuti'

    def __str__(self):
        return self.title
