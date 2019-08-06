from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    re_path(r'^search$', views.partial_search, name='PartialSearch'),
]