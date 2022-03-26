from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addauction", views.addauction, name="addauction"),
    path("listing/<str:id>", views.show_listing, name="show_listing"),
    path("comment", views.add_comment, name="add_comment"),
    path("bid", views.bid, name="bid"),
    path("watch/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watch/list", views.watchlist, name="list_watchlist"),
    path("sort/select",views.show_sort_template, name="show_sort_template"),
    path("sort/by/<str:category>", views.sort, name="sort"),
    path("closeauction",views.close_auction, name="close_auction")
]
