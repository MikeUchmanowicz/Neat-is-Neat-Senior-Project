from django.shortcuts import render
from django.http import HttpResponse

from Demo.exceptions import db_operational_handler
from . services import AIDataService

# RETRIEVES ALL DATA MODELS AND RETURNS THEM TO VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
def readDemoInfo(response):
    datalist = AIDataService.retrieveAllGens()
    return render(response, "demo/demoInfo.html", {"aidatalist":datalist})

# @db_operational_handler # EXCEPTION HANDLER WRAPPER FUNCTION
# def sortDemoInfo(response, value:str):    
#     datalist = AIDataService.retrieveAllGens().order_by(value)
#     return render(response, "demo/demoInfo.html", {"aidatalist":datalist})

def sortDemoInfo(request):
    
    if request.method == 'POST':
        sortBy=request.POST.get('SortBy')
        orderBy:str = request.POST.get('OrderBy')
        
        if orderBy == "ascending":
            orderBy = ""
        else:
            orderBy = "-"
        
        datalist = AIDataService.retrieveAllGens().order_by(orderBy+(sortBy))
    else:
        datalist = AIDataService.retrieveAllGens()
    
    return render(request, "demo/demoInfo.html", {"aidatalist":datalist})