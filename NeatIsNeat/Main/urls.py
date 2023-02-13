from django.urls import path
from . import views

#URLS FOR MAIN APP, MAPS URLS TO VIEWS
urlpatterns = [
    path("", views.home, name="home"),
    path("neatInfo", views.neatInfo, name="neatInfo"),
    path("gameInfo", views.gameInfo, name="gameInfo"),
]

