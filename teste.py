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

import autres.ortiz.ia as ia

#teste git#

## Creation d'une equipe

pyteam = module.get_team(2)
thon = ia.get_team(2)

#pyteam = SoccerTeam(name = "GermanyWins")
#thon = SoccerTeam(name = "BRBRBR")

#pyteam.add("P1", module.DribleStrat())
#pyteam.add("P2", module.DefStratOpt())
#thon.add("P3", module.DefStratOpt())
#thon.add("P4", module.ShootStrat())

#Creation d'une partie
simu = Simulation(pyteam, thon)

#Jouer et afficher la partie
show_simu(simu)
