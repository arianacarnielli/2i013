# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:14:13 2018

@author: arian
"""

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

#import autres.ortiz.ia as ia
#import autres.sebastien.footIA as ia
#import autres.austenprinciple.Foot as ia
#import autres.ahmedmelliti.module as ia
#import autres.caieddy.module as ia
#import autres.iamlisa.module as ia 
#import autres.baladeur.modulesocc as ia
#import autres.aatarek.RepoSoccer_master as ia
import autres.chefifarouck.FarouckYann as ia

#teste git#

## Creation d'une equipe

thon = module.get_team(1)
pyteam = ia.get_team(1)


#pyteam = SoccerTeam(name = "GermanyWins")
#thon = SoccerTeam(name = "BRBRBR")

#pyteam.add("P1", module.DribleStrat())
#pyteam.add("P2", module.DefStratOpt())
#thon.add("P3", module.DefStratOpt())
#thon.add("P4", module.ShootStrat())

#Creation d'une partie
simu = Simulation(thon, pyteam)

#Jouer et afficher la partie
show_simu(simu)

