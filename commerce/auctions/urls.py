from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("close_bid/<str:title>", views.close_bid, name="close_bid"),
    path("comment/<str:title>", views.comment, name="comment"),
    path("categories/", views.categories, name="categories"),
    path("categories/category/<str:category>", views.category, name="category"),
    path("watch_list/", views.watch_list, name="watch_list"),
    path("search/", views.search, name="search")
]
