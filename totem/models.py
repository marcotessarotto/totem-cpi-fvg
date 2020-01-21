import datetime

from django.db import models
from django.utils import timezone

#datetime e timezone utili nel caso di funzioni sulle date
# come da tutorial


class Area(models.Model):
    area_name = models.CharField(max_length=50)

    def __str__(self):
        return self.area_name
    # utile per prompt e rappresentazione su admin


class Content(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    # valutare massimo di postgreSQL e TextField in alternativa
    pub_date = models.DateTimeField('date published')
    update = models.DateTimeField('last update')

    def __str__(self):
        return self.content
