from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.forms import (
    CheckboxSelectMultiple,
    TextInput
)
# from ckeditor.fields import RichTextField
# from django import forms

from .models import *

admin.site.site_header = f'backoffice Totem-cpi'

admin.site.register(Category)
admin.site.register(FileItem)
admin.site.register(MapZone)


# class AreaAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = Area
#         fields = '__all__'


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin,):
    list_display = ('id', 'title', )
    # form = AreaAdminForm

    def add_default_areas(self, request):

        result = Area.fill_default_areas()

        if result:
            self.message_user(request, "le aree di default sono state aggiunte")
        else:
            self.message_user(request, "non ho fatto nulla, ci sono già aree presenti")

        from django.http import HttpResponseRedirect
        return HttpResponseRedirect("../")

    add_default_areas.short_description = "Aggiungi le aree di default"

    change_list_template = "areas/areas_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        my_urls = [
            path('add_default_areas/', self.add_default_areas),
        ]
        return my_urls + urls


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
