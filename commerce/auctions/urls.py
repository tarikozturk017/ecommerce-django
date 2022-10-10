from django.urls import path

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
    path("comment/<str:title>", views.comment, name="comment")
]
