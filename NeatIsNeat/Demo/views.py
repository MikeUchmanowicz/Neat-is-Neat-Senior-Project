from django.shortcuts import render

from Demo.exceptions import db_operational_handler
from . services import AIDataService

# Create your views here.
@db_operational_handler # EXCEPTION HANDLER
def demoInfo(response):
    data = AIDataService.retrieveAllGens()
    return render(response, "demo/demoInfo.html", {"datalist":data})