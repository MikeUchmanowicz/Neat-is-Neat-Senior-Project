from . models import DataModel 

#CLASS USED TO RETRIEVE DATA MODELS FROM PYTHON GAME SCRIPT
class AIDataService():
        
    #RETRIEVE ALL DATA MODELS
    def retrieveAllGens():
        data = DataModel.objects.all()
        list(data)
        return data
        