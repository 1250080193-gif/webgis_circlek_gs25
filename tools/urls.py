from django.urls import path
from . import views

urlpatterns = [
    path("stores-in-bounds/", views.stores_in_bounds),
    path("stores-in-radius/", views.stores_in_radius),
    path("smart-search/", views.smart_search),

    path("reverse-geo/", views.reverse),
    path("suggest/", views.suggest),
    path("districts/", views.districts),
    path("search-stores/", views.search_stores),

    path("route-osrm/", views.route_osrm),
    path("ping/", views.ping),
]
