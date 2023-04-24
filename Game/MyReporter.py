from statistics import mean, stdev
import time
import neat
from neat import six_util
import GameModels as models
from DataAccess import AIDAO

class myReporter(neat.StdOutReporter):
    
    def __init__(self, show_species_detail, useDatabase):
        self.useDatabase = useDatabase
        self.show_species_detail = show_species_detail
        self.generation = None
        self.generation_start_time = None
        self.generation_times = []
        self.num_extinctions = 0
        
        if self.useDatabase:
            ##############################################################################
            print("AIDAO.deleteAllGen()")
            AIDAO.deleteAllGen()
            ##############################################################################
        
    def post_evaluate(self, config, population, species, best_genome):
        print ("\n START POST EVAL \n")
        ng = len(population)
        # pylint: disable=no-self-use
        fitnesses = [c.fitness for c in six_util.itervalues(population)]
        fit_mean = mean(fitnesses)
        fit_std = stdev(fitnesses)
        best_species_id = species.get_species_id(best_genome.key)
        print('Population\'s average fitness: {0:3.5f} stdev: {1:3.5f}'.format(fit_mean, fit_std))
        print(
            'Best fitness: {0:3.5f} - size: {1!r} - species {2} - id {3}'.format(best_genome.fitness,
                                                                                best_genome.size(),
                                                                                best_species_id,
                                                                                best_genome.key))
        
        elapsed = time.time() - self.generation_start_time
        self.generation_times.append(elapsed)
        self.generation_times = self.generation_times[-10:]
        average = sum(self.generation_times) / len(self.generation_times)
        print('Total extinctions: {0:d}'.format(self.num_extinctions))
        if len(self.generation_times) > 1:
            print("Generation time: {0:.3f} sec ({1:.3f} average)".format(elapsed, average))
        else:
            print("Generation time: {0:.3f} sec".format(elapsed))
        
        # INSERTED CODE TO EXTENSION    

        sids = list(six_util.iterkeys(species.species))
        sids.sort()

        for sid in sids:
            s = species.species[sid]
            a = self.generation - s.created
            n = len(s.members)
            f = "--" if s.fitness is None else "{:.1f}".format(s.fitness)
            af = "--" if s.adjusted_fitness is None else "{:.3f}".format(s.adjusted_fitness)
            st = self.generation - s.last_improved
            
            """ 
                gen = a
                popSize = n
                avgFit = fit_mean
                stdDevFit = fit_std
                bestFit = f
                adjFit = af
                stag = st
            """
            d=models.DataModel(self.generation,n,round(fit_mean, 3), round(fit_std, 3), best_genome.fitness, af, st)
            
        if self.useDatabase:    
            ##############################################################################
            print("AIDAO.insertOneGen(d)")    
            AIDAO.insertOneGen(d)
            ##############################################################################    
            
            print ("\n END POST EVAL \n")  
        
        

    