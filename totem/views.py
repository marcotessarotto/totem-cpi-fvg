from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.views import generic

from .models import Area, Content, UserAction, Informations


def content(request, content_id):
    if not request.session.session_key:
        request.session.create()

    print(request.session.session_key)

    ua = UserAction()
    ua.content_id = content_id
    ua.session_id = request.session.session_key
    ua.save()

    # content_text = Content.objects.all()
    content_text = get_object_or_404(Content, id=content_id)
    # content_text = Content.objects.get(pk=content_id)
    linked_content = Content.objects.filter(linked_contents__id=content_id)
    # linked_content = #get_object_or_404(Content, id=content_id)

    context = {'content_text': content_text,
               'linked_content': linked_content}
    return render(request, 'totem/content.html', context)


def info(request, info_id):
    area_id = request.GET.get('area_id', '-')
    content_id = request.GET.get('content_id', '-')

    # print(area_id)
    # print(content_id)

    info_text = get_object_or_404(Informations, id=info_id)
    content_instance = get_object_or_404(Content, id=content_id)

    context = {'info_text': info_text,
               'content': content_instance}

    return render(request, 'totem/info.html', context)


def mappa(request):
    return render(request, 'totem/map.html', {})

def prova(request):
    areas = []
    for area in Area.objects.order_by('id'):
        queryset = Content.objects.filter(area=area).order_by('id')

        area.contents = queryset
        areas.append(area)

    context = {'areas': areas}

    return render(request, 'totem/prova.html', context)



class IndexView(generic.View):

    def get(self, request, *args, **kwargs):

        if not request.session.session_key:
            request.session.create()
            request.session.set_expiry(120)  # set http session timeout (seconds)

            print(f"new sessionid: {request.session.session_key}")
        else:
            print(f"existing sessionid: {request.session.session_key}")

        ua = UserAction()
        ua.session_id = request.session.session_key
        # ua.action_type =
        ua.save()

        areas = []
        for area in Area.objects.order_by('id'):
            queryset = Content.objects.filter(area=area).order_by('id')

            area.contents = queryset
            areas.append(area)

        context = {'areas': areas}

        return render(request, 'totem/homepage.html', context)
