from django.urls import path

from . import views

app_name = 'totem'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('content/<int:content_id>/', views.content, name='content'),
    path('info/<int:info_id>/', views.info, name='info'),
    #path('<int:content_id>/content/<int:info_id>/info', views.info, name='info'),

    path('map', views.mappa, name='map'),
]