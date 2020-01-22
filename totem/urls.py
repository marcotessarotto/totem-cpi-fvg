from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # path('', views.index, name='index'),
    # # totem/17/ (con barra finale)
    # path('<int:area_id>/', views.area, name='area'),
    # # totem/17/content
    # path('<int:content_id>/content', views.content, name='content'),
]