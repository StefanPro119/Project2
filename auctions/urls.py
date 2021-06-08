from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name='create'),
    path("detail/<int:item_id>/", views.auction_item, name='item'),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("watchlist/<int:item_id>/", views.add_to_watchlist, name='add_to_watchlist'),
    path("make_bid/<int:item_id>/", views.make_bid, name='make_bid'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
