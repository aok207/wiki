from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>", views.wiki_page, name="wiki"),
    path("new/", views.new_page, name="new"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random")
]
