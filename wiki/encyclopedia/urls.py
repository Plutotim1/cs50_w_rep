from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.show_entry, name="show_entry"),
    path("random", views.random, name="random"),
    path("add", views.add, name='add'),
    path("wiki/edit/<str:entry_name>", views.edit_entry, name="edit_entry"),
    path("search/", views.search, name="search")
]
