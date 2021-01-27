import numpy as np
from numpy import random as ran

class TASEP(): # this is a parent class of TASEP parallel and random shuffle models
    
    def __init__(self, length, number_of_particles, time):
        self.length = length   # length of lattice
        self.number_of_particles = number_of_particles   # number of particles in lattice
        self.time = time       # when will the simulation end
        self.cell_index = length//2  # index of cell where we will be monitoring whether the particle is in or not
        
    def initial_condition(self, p, alpha, beta):
        self.p = p          # probability, that the particle will move left
        self.alpha = alpha    # probability that particle will enter lattice
        self.beta = beta    # probability that particle will leave lattice
        
        aux = ran.default_rng().choice(self.length, size=self.number_of_particles, replace=False) # randomly chooses where the initial particles will be placed
        self.lattice = np.concatenate((np.array([True]),([True if i in aux else False for i in range(self.length)]))) # places the initial particles and creates an extra beginner spot for inflow condition
        self.density = [] # the density will be saved here, we are not saving the initial condition
        self.monitored_cell = [self.lattice[self.cell_index]] # here will be saved the value in the cell with index cell_index
        
    def save_variables(self): # saves the current density and value of cell with index cell_index
        self.density.append(self.number_of_particles/self.length)
        self.monitored_cell.append(self.lattice[self.cell_index])
            
    def update_rule(self): # sets up order in which the particles will move
        pass      
    
    def hop(self, i): # handles movement of one particle
        pass
            
    def streaming(self): # moves all particles
        for i in self.update_rule():
            self.hop(i)
            
    def algorithm(self): # the algorithm of TASEP, in one time step it moves all particles and saves lattice to history, repeats till the simulation ends
        t = 0
        while t < self.time:
            self.streaming()
            self.save_variables()
            t += 1
            
    def get_result(self): # returns density and current particle flow density
        current_particle_flow_density = [1 if (self.monitored_cell[i-1] == True) & (self.monitored_cell[i] == False) else 0 for i in range(1,self.time+1)]
        return np.array(self.density), np.array(current_particle_flow_density)
            
    def execute(self, p, alpha, beta): # executes the simulation
        self.initial_condition(p, alpha, beta)
        self.algorithm()
        return self.get_result()
            

class TASEP_Parallel(TASEP): # parallel model for TASEP
            
    def update_rule(self):
        res = [i for i in range(len(self.lattice)-1) if (self.lattice[i] and not self.lattice[i+1])]
        if self.lattice[len(self.lattice)-1]:
            res.append(len(self.lattice)-1)
        return np.array(res)       
    
    def hop(self, i):
        if i == len(self.lattice)-1:
            if ran.random() < self.beta:
                self.lattice[i] = False
                self.number_of_particles -= 1
        elif i == 0:
            if ran.random() < self.alpha:
                self.lattice[i+1] = True;
                self.number_of_particles += 1
        else:
            if ran.random() < self.p:
                self.lattice[i] = False
                self.lattice[i+1] = True
                
                
class TASEP_Random(TASEP): # random shuffle model for TASEP
     
    def update_rule(self):
        particles = [i for i in range(len(self.lattice)) if self.lattice[i]]
        order = ran.default_rng().choice(len(particles), size=len(particles), replace=False)
        return [particles[np.where(order == i)[0][0]] for i in range(len(order))]
            
    def hop(self, i):
        if i == len(self.lattice)-1:
            if ran.random() < self.beta:
                if self.lattice[i] == True: self.number_of_particles -= 1
                self.lattice[i] = False
        elif i == 0:
            if ran.random() < self.alpha:
                if self.lattice[i+1] == False: self.number_of_particles += 1
                self.lattice[i+1] = True;
        else:
            if not self.lattice[i+1] and ran.random() < self.p:
                self.lattice[i] = False
                self.lattice[i+1] = True
