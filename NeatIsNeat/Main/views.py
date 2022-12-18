from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

#HOME VIEW
def home(response):
    return render(response, "main/home.html")

#NEATINFO VIEW
def neatInfo(response):
    return render(response, "main/neatInfo.html")

#GAMEINFO VIEW
def gameInfo(response):
    return render(response, "main/gameInfo.html")    





