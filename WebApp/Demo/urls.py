
from django.urls import path
from . import views

#DEMO APP URLS, MAPS URLS TO VIEWS
urlpatterns = [
    path("demoInfo/", views.readDemoInfo, name="demoInfo"),
    path("demoInfo/sort/", views.sortDemoInfo, name="sortDemoInfo")
]

"""
    path("example/", views.example, name="example"),
    path("passVar/<str:fname>", views.passVar, name="passVar")
"""