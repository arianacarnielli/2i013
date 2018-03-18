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


import autres.ortiz.ia as ia
#import autres.sebastien.footIA as ia
#import autres.austenprinciple.Foot as ia
#import autres.ahmedmelliti.module as ia
#import autres.caieddy.module as ia
#import autres.iamlisa.module as ia 
#import autres.baladeur.modulesocc as ia
#import autres.aatarek.RepoSoccer_master as ia
#import autres.chefifarouck.FarouckYann as ia


                
def genVectAleaStratDribleur():
    accShoot = rd.randrange(0, 10, 1) / 10.
    accDrible = rd.randrange(0, 10, 1) / 10.
    vit = rd.randrange(0, 10, 1) / 10.
    n = rd.randrange(0, 20, 1)
    maxAngle = round(rd.uniform(0, math.pi/2), 2)
    tooFar = rd.randrange(0, 60, 1)
    rSurfBut = rd.randrange(0, 50, 5)
    AngleHyst = round(rd.uniform(0, math.pi/10), 2)
    
    return [accShoot, accDrible, vit, n, maxAngle, tooFar, rSurfBut, AngleHyst]
    
    
    
    
class ParamSearch_gen(object):
    def __init__(self, strategy1, strategy2, simu=None, trials=20, max_steps=1000000, max_round_step=400):
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.simu = simu
        self.trials = trials
        self.max_steps = max_steps
        self.max_round_step = max_round_step

        self.params = genVectAleaStratDribleur()        
                

    def start(self, show=True):
        if not self.simu:
            print (self.params)
            brasil = SoccerTeam("Brasil")
            brasil.add("self.strategy1", self.strategy1(p = 0.8))
            brasil.add("self.strategy2", self.strategy2(accShoot = self.params[0], accDrible = self.params[1], vit = self.params[2], n = self.params[3], maxAngle = self.params[4], tooFar = self.params[5], rSurfBut = self.params[6], AngleHyst = self.params[7]))
               
            desafiante = ia.get_team(2)
        
            self.simu = Simulation(brasil, desafiante, max_steps=self.max_steps)
            
        self.simu.listeners += self #Q Q É ISSO AQUI???

        if show:
            show_simu(self.simu)
        else:
            self.simu.start()

    def begin_match(self, team1, team2, state):
        self.last = 0  # Step of the last round
        self.crit1 = 0  # Criterion 1 to maximize (here, number of goals by team 1)
        self.crit2 = 0  # Criterion 2 to minimize (here, number of goals by team 2)
        self.cpt = 0  # Counter for trials

      
    def update_round(self, team1, team2, state):
        # Stop the round if it is too long
        if state.step > self.last + self.max_round_step:
            self.simu.end_round()

    def end_round(self, team1, team2, state):
        # A round ends when there is a goal
        if state.goal == 1:
            self.crit1 += 1  # Increment criterion
        elif state.goal == 2:
            self.crit2 += 1

        self.cpt += 1  # Increment number of trials
        
      
        if self.cpt >= self.trials:
            self.simu.end_match()


    def get_res(self):
        return self.res
