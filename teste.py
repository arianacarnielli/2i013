# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:17:23 2018

@author: 3525837
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player, show_simu, Simulation
from soccersimulator.settings import *
from soccersimulator import Strategy

from module.strategy import *

import math

## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")
pyteam.add("PyPlayer",ShootBallStrategy())
#thon.add("ThonPlayer",ShootStrategy())   #Strategie aleatoire0.

#Creation d'une partie
simu = Simulation(pyteam,thon)


#Jouer et afficher la partie
show_simu(simu)
