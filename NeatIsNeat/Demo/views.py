import string
from django.shortcuts import render

from Demo.exceptions import db_operational_handler
from . services import AIDataService

# RETRIEVES ALL DATA MODELS AND RETURNS THEM TO VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def demoInfo(response):
    aidata = AIDataService.retrieveAllGens()
    labels = []
    fits = []
    gens = []
    
    for data in aidata:
        fits.append(data.bestFit)
        gens.append(data.gen)
        labels.append("Gen " +str(data.gen))
    
    return render(response, "demo/demoInfo.html", {"aidatalist":aidata, "labels":labels, "fit":fits, "gen":gens})