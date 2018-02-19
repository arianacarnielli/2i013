# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:17:23 2018

@author: 3525837
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player, show_simu, Simulation
from soccersimulator.settings import *
from soccersimulator import Strategy

import module

import math

## Creation d'une equipe

pyteam = module.get_team(2)
thon = SoccerTeam(name="ThonTeam")


thon.add("ThonPlayer",module.PassStrat())  
thon.add("ThonPlayer2",module.DefStratOpt(0.1)) 

#Creation d'une partie
simu = Simulation(pyteam, thon)


#Jouer et afficher la partie
show_simu(simu)
