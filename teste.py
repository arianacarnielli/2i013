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

#pyteam.add("P1", module.DribleStratOpt())
pyteam.add("D", module.DribleStratOpt2(accShoot = 0.64, accDrible = 0.15, vit = 1, n = 0, maxAngle = 0.76, tooFar = 53, rSurfBut = 45, AngleHyst = 0.07, distShoot = 50))
        
thon.add("Adv", module.ShootStrat())


#Creation d'une partie
simu = Simulation(pyteam, thon)

#Jouer et afficher la partie
show_simu(simu)
