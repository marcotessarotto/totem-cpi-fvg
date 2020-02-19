import datetime

from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from colorful.fields import RGBColorField

LANGUAGES = (
    ('it', 'Italiano'),
    ('en', 'English'),
    ('slo', 'Slovenski jezik'),
    ('de', 'Deutsche sprache'),
    ('hrv', 'Hrvatski jezik'),
)

USER_ACTIONS = (
    (-1, '-'),
    (0, 'index'),
    (1, 'area'),
    (2, 'content'),
    (3, 'information')
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


class Office(models.Model):
    title = RichTextField(max_length=1024, verbose_name="nome dell'ufficio")

    class Meta:
        verbose_name = 'Ufficio'
        verbose_name_plural = 'Uffici'
    def __str__(self):
        return "Office " + str(self.id) + ' (' + \
               str(self.title) + ') '


class MapZone(models.Model):
    title = RichTextField(max_length=1024, verbose_name="nome della zona")

    color = RGBColorField(blank=True, null=True, )

    floor = models.CharField(max_length=1024, blank=True, null=True, verbose_name="piano")

    tag = models.CharField(max_length=1024, blank=True, null=True, verbose_name="tag identificativo")

    description = RichTextField(max_length=1024, blank=True, null=True, verbose_name="descrizione")

    class Meta:
        verbose_name = 'Zona della mappa'
        verbose_name_plural = 'Zone della mappa'

    def __str__(self):
        return "MapZone " + str(self.id) + ' (' + \
               str(self.tag) + ') '


class Area(models.Model):
    title = RichTextField(max_length=1024, verbose_name="nome dell'area")

    color = RGBColorField(blank=True, null=True, )

    office = models.ForeignKey(Office, on_delete=models.PROTECT, blank=True, null=True, verbose_name="dove?")

    image = models.ForeignKey(FileItem, on_delete=models.PROTECT, null=True, blank=True, verbose_name="immagine")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data inserimento')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Aree'

    def __str__(self):
        return self.title

    @staticmethod
    def fill_default_areas():
        print("fill_default_areas")

        if len(Area.objects.all()) != 0:
            return False

        a = Area()
        a.title = "Accoglienza informazioni"
        a.save()

        a = Area()
        a.title = "Colloqui individuali"
        a.save()

        a = Area()
        a.title = "Laboratori di gruppo"
        a.save()

        a = Area()
        a.title = "Servizio incontro domanda offerta"
        a.save()

        a = Area()
        a.title = "Attivazione tirocini"
        a.save()

        return True


class Informations(models.Model):
    # area = models.ForeignKey(Area, on_delete=models.PROTECT, blank=True, null=True, verbose_name="area")
    where = models.ForeignKey(MapZone, on_delete=models.PROTECT, blank=True, null=True, verbose_name="dove?")
    when = RichTextField(max_length=1024, blank=True, null=True, verbose_name="quando?")
    how = RichTextField(max_length=1024, blank=True, null=True, verbose_name="come?")
    for_who = RichTextField(max_length=1024, blank=True, null=True, verbose_name="per chi?")

    class Meta:
        verbose_name = 'Informazioni'
        verbose_name_plural = 'Informazioni'

    def __str__(self):
        return "Info " + str(self.id)


class Content(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    title = RichTextField(max_length=1024, blank=True, null=True, verbose_name="titolo")
    # title = models.CharField(max_length=1024, blank=True, null=True, verbose_name="titolo")
    text = RichTextField(max_length=4096, blank=True, null=True, )

    image = models.ForeignKey(FileItem, on_delete=models.PROTECT, null=True, blank=True, verbose_name="immagine")

    categories = models.ManyToManyField(Category, blank=True, verbose_name="categorie")

    link = models.CharField(max_length=1024, blank=True, null=True)
    link_caption = models.CharField(max_length=1024, blank=True, null=True, default="continua")

    lang = models.CharField(max_length=3, choices=LANGUAGES, default='it',
                            verbose_name="lingua")

    linked_contents = models.ManyToManyField('Content', blank=True, verbose_name="contenuti collegati")

    level = models.SmallIntegerField(default=1)

    information = models.ForeignKey(Informations, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name="dove, come, quando, per chi?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data inserimento')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contenuto'
        verbose_name_plural = 'Contenuti'

    def __str__(self):
        return self.title


class UserAction(models.Model):
    session_id = models.CharField(max_length=64, blank=True, null=True)
    content_id = models.SmallIntegerField(default=-1)
    information_id = models.SmallIntegerField(default=-1)
    mapzone_id = models.SmallIntegerField(default=-1)

    # action_type = models.SmallIntegerField(default=-1, choices=USER_ACTIONS, default=-1)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data inserimento')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.session_id)
