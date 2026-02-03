from django.shortcuts import render

def home(request):
    return render(request, "gis_store/home.html")

def store_list_page(request):
    return render(request, "gis_store/store_list.html")

def map_page(request):
    return render(request, "gis_store/map.html")

