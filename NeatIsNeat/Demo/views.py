from django.shortcuts import render

from Demo.exceptions import db_operational_handler
from . services import AIDataService

# RETRIEVES ALL DATA MODELS AND RETURNS THEM TO VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def readDemoInfo(response):
    datalist = AIDataService.retrieveAllGens()
    return render(response, "demo/demoInfo.html", {"aidatalist":datalist})

@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def sortDemoInfo(response, value:str):    
    datalist = AIDataService.retrieveAllGens().order_by(value)
    return render(response, "demo/demoInfo.html", {"aidatalist":datalist})