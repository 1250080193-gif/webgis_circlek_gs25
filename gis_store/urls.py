from django.urls import path
from . import views

app_name = "gis_store"

urlpatterns = [
    path("", views.home, name="home"),
    path("stores/", views.store_list_page, name="stores_page"),
    path("map/", views.map_page, name="map_page"),
]
