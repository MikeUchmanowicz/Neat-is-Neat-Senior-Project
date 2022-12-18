
from django.urls import path
from . import views

#URLS FOR MAIN APP
urlpatterns = [
    path("", views.home, name="home")
]

