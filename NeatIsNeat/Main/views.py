from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

#HOME VIEW, Redirects to home.html
def home(response):
    return render(response, "main/home.html")

#NEATINFO VIEW, Redirects to neatInfo.html
def neatInfo(response):
    return render(response, "main/neatInfo.html")

#GAMEINFO VIEW, Redirects to gameInfo.html
def gameInfo(response):
    return render(response, "main/gameInfo.html")    





