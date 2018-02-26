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

#teste git#

## Creation d'une equipe

#pyteam = module.get_team(4)

pyteam = SoccerTeam(name = "GermanyWins")
thon = SoccerTeam(name = "BRBRBR")

pyteam.add("P1", module.PassStrat())
pyteam.add("P1b", module.PassStrat())
pyteam.add("P2", module.DefStratOpt())
thon.add("P3", module.ShootStrat())
thon.add("P4", module.DefStratOpt())

#Creation d'une partie
simu = Simulation(pyteam, thon)

#Jouer et afficher la partie
show_simu(simu)
