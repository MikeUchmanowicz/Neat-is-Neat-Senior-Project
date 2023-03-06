from django.shortcuts import render
from django.http import HttpResponse

from Demo.exceptions import db_operational_handler
from . services import AIDataService

# RETRIEVES ALL DATA MODELS AND RETURNS THEM TO VIEW, REDIRECTS TO demoInfo.html
@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def readDemoInfo(response):
    datalist = AIDataService.retrieveAllGens()
    return render(response, "demo/demoInfo.html", {"aidatalist":datalist})

# RETRIEVES ALL DATA MODELS AND RETURNS THEM TO VIEW, OBTAINS SORTING PARAMETERS FROM POST REQUEST, REDIRECTS TO demoInfo.html
@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def sortDemoInfo(request):
    
    if request.method == 'POST':
        sortBy=request.POST.get('SortBy')       # GETS SORTING PARAMETER FROM POST REQUEST
        orderBy:str = request.POST.get('OrderBy')
        
        if orderBy == "ascending":
            orderBy = ""
        else:
            orderBy = "-"
                                                # SORTS DATA MODELS BY SORTING PARAMETER
        datalist = AIDataService.retrieveAllGens().order_by(orderBy+(sortBy))
    else:
        datalist = AIDataService.retrieveAllGens()
    
    return render(request, "demo/demoInfo.html", {"aidatalist":datalist})