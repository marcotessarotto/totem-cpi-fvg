from django.contrib import admin
from django.forms import (
    CheckboxSelectMultiple,
    TextInput
)

from .models import *

admin.site.site_header = f'backoffice Totem-cpi'

admin.site.register(Category)
admin.site.register(FileItem)

admin.site.register(Area)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin,):

    list_display = ('id', 'title', 'list_of_categories', 'area',  )
    # exclude = ('like', 'dislike')
    search_fields = ('id', 'title')
    list_filter = ('categories',)
    actions = ["export_as_csv"]

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},

        # https://stackoverflow.com/questions/910169/resize-fields-in-django-admin
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
        #        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},

    }

    def list_of_categories(self, obj):
        return ', '.join([a.name for a in obj.categories.all()])

    list_of_categories.short_description = "Categorie"
