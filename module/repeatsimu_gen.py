# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:41:23 2018

@author: 3525837
"""

from __future__ import print_function, division
from soccersimulator import SoccerTeam, Simulation, Strategy, show_simu, Vector2D
from soccersimulator.settings import *


from .action import *
from .toolbox import *
from .strategy import *
from .comportement import *


import random as rd
import math
import numpy as np

    
class repeatsimu_gen2V2(object):
    def __init__(self, list_param, ia, trials=20, max_steps=2000):
        self.strategy1 = DefIntelligentStratOpt
        self.strategy2 = DribleStratOpt2
        self.trials = trials
        self.max_steps = max_steps
        
        self.list_param = list_param
        self.ia = ia
        
        self.results = np.empty((self.trials, 2), dtype = int)
               

    def start(self, show = False, verbose = True):
        self.results = np.empty((self.trials, 2), dtype = int)
        for i in range(self.trials):
            if verbose:
                print(" Match",i)
            brasil = SoccerTeam("Brasil")
            brasil.add("self.strategy1", self.strategy1(p = self.list_param[9], n = self.list_param[10], alpha = self.list_param[11], distMin = self.list_param[12], distMax = self.list_param[13], maxAngle = self.list_param[14], rayon = self.list_param[15]))
            brasil.add("self.strategy2", self.strategy2(accShoot = self.list_param[0], accDrible = self.list_param[1], vit = self.list_param[2], n = self.list_param[3], maxAngle = self.list_param[4], tooFar = self.list_param[5], rSurfBut = self.list_param[6], AngleHyst = self.list_param[7], distShoot = self.list_param[8]))
               
            desafiante = self.ia.get_team(2)
        
            simu = Simulation(brasil, desafiante, max_steps=self.max_steps)

            if show:
                show_simu(simu)
            else:
                simu.start()
            
            self.results[i, 0] = simu.get_score_team(1)
            self.results[i, 1] = simu.get_score_team(2)
            if verbose:
                print(" Score : {} x {}".format(self.results[i, 0], self.results[i, 1]))
        
    def get_result(self):
        return self.results.sum(axis = 0)
    
    def get_points(self):
        return 3*(self.results[:, 0] > self.results[:, 1]).sum() + \
                 (self.results[:, 0] == self.results[:, 1]).sum() 
                 
class repeatsimu_gen1V1(object):
    def __init__(self, list_param, ia, trials=20, max_steps=2000):
        self.strategy = Drible1vs1StratOpt2
        self.trials = trials
        self.max_steps = max_steps
        
        self.list_param = list_param
        self.ia = ia
        
        self.results = np.empty((self.trials, 2), dtype = int)
               

    def start(self, show = False, verbose = True):
        self.results = np.empty((self.trials, 2), dtype = int)
        for i in range(self.trials):
            if verbose:
                print(" Match",i)
            brasil = SoccerTeam("Brasil")
            brasil.add("self.strategy", self.strategy(accShoot = self.list_param[0], accDrible = self.list_param[1], vit = self.list_param[2], n = self.list_param[3], maxAngle = self.list_param[4], tooFar = self.list_param[5], rSurfBut = self.list_param[6], AngleHyst = self.list_param[7]))
               
            desafiante = self.ia.get_team(1)
        
            simu = Simulation(brasil, desafiante, max_steps=self.max_steps)

            if show:
                show_simu(simu)
            else:
                simu.start()
            
            self.results[i, 0] = simu.get_score_team(1)
            self.results[i, 1] = simu.get_score_team(2)
            if verbose:
                print(" Score : {} x {}".format(self.results[i, 0], self.results[i, 1]))
        
    def get_result(self):
        return self.results.sum(axis = 0)
    
    def get_points(self):
        return 3*(self.results[:, 0] > self.results[:, 1]).sum() + \
                 (self.results[:, 0] == self.results[:, 1]).sum() 