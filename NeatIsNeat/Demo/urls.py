
from django.urls import path
from . import views

#DEMO APP URLS
urlpatterns = [
    path("demoInfo/", views.readDemoInfo, name="demoInfo"),
    path("demoInfo/sort/<str:value>", views.sortDemoInfo, name="sortDemoInfo")
]

"""
    path("example/", views.example, name="example"),
    path("passVar/<str:fname>", views.passVar, name="passVar")
"""