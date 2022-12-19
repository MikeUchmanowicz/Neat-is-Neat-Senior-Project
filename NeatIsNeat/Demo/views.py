from django.shortcuts import render

from Demo.exceptions import db_operational_handler
from . services import AIDataService

# RETRIEVES ALL DATA MODELS AND RETURNS THEM TO VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def demoInfo(response):
    data = AIDataService.retrieveAllGens()
    return render(response, "demo/demoInfo.html", {"datalist":data})