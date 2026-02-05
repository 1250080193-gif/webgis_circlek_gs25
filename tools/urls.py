from django.urls import path
from . import views

urlpatterns = [
    # path("debug-geocode/", views.debug_geocode),
    path("stores-in-bounds/", views.stores_in_bounds),
    path("stores-in-radius/", views.stores_in_radius),
    path("smart-search/", views.smart_search),
]
