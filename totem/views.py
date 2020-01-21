from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import Area, Content

def index(request):
    area_list = Area.objects.order_by('-area_name')[:5]
    context = {'area_list': area_list}
    return render(request, 'totem/index.html', context)
    #area_list = Area.objects.order_by('-area_name')[:5]
    #output = ', '.join([q.area_name for q in area_list])
    #return HttpResponse(output)


def area(request, area_id):
    title = Content.objects.get(pk=area_id)
    #print(title)
    return HttpResponse("Stai vedendo MACROAREA %s." % title)

def content(request, content_id):

    #content_text = Content.objects.all()
    content_text = Content.objects.get(pk=content_id)
    context = {'content_text' : content_text}
    return  render(request, 'totem/content.html',context)

    #return HttpResponse("Sei su CONTENUTO %s." % content_id)