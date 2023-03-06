from django.db import connections, models
from enum import auto

#DATA MODEL (USED BY PYTHON GAME SCRIPT)
class DataModel(models.Model):  
    
    gen = models.AutoField(primary_key=True, editable=False)
    popSize = models.IntegerField()
    avgFit = models.FloatField()
    stdDevFit = models.FloatField()
    bestFit = models.FloatField()
    adjFit = models.FloatField()
    stag = models.IntegerField()
    
    #TOSTRING   
    def __str__(self):
        return('gen: {0}\npopSize: {1}\navgFit: {2}\nstdDevFit: {3}\nbestFit: {4}\nadjFit: {5}\nstag: {6}\n'.format(self.gen,self.popSize,self.avgFit,self.stdDevFit,self.bestFit,self.adjFit,self.stag))



