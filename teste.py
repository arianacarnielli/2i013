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
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")

pyteam.add("PyPlayer",module.DefNaifStrategy())
#pyteam.add("PyPlayer2",module.ShootBallStrategyOptimal())

thon.add("ThonPlayer",module.DefNaifStrategy())  
#thon.add("ThonPlayer2",module.ShootBallStrategyOptimal()) 

#Creation d'une partie
simu = Simulation(pyteam,thon)


#Jouer et afficher la partie
show_simu(simu)
