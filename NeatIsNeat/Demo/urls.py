
from django.urls import path
from . import views

#DEMO APP URLS
urlpatterns = [
    path("demoInfo/", views.demoInfo, name="demoInfo")
]

"""
    path("example/", views.example, name="example"),
    path("passVar/<str:fname>", views.passVar, name="passVar")
"""