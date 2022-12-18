from django.shortcuts import render
from . services import AIDataService

# Create your views here.
def demoInfo(response):
    data = AIDataService.retrieveAllGens()
    return render(response, "demo/demoInfo.html", {"datalist":data})