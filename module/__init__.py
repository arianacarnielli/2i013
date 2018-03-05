# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:29:15 2018

@author: 3525837
"""
from .action import *
from .toolbox import *
from .strategy import *
from .comportement import *
from .optimization import *
from .optimization_gen import *
    
import math
    
def get_team(nb_players):
    myteam = SoccerTeam(name="Brasil")
    if nb_players == 1:
        myteam.add("RRRRONALDO", Drible1vs1StratOpt2(n = 18, maxAngle = math.pi/4, tooFar = 10*maxBallAcceleration))
    if nb_players == 2:
        #myteam.add("Joueur 1", ShootBallStratOpt(acc = 1))
        myteam.add("Cafu", Def2StratOpt(p = 0.8))
        myteam.add("RRRRONALDO", DribleStratOpt2(n = 18, accShoot = 0.25, maxAngle = math.pi/4, tooFar = 9*maxBallAcceleration))

    if nb_players == 4:
        myteam.add("Joueur 1",ShootBallStratOpt(acc = 1))
        myteam.add("Joueur 2",DefStratOpt(0.7))
        myteam.add("Joueur 3",DribleStrat())
        myteam.add("Joueur 4",DefStratOpt(0.7))
    return myteam	

def get_team_challenge(num):
    myteam = SoccerTeam(name="Brasil")
    if num == 1:
        myteam.add("Joueur Chal "+str(num),ShootBallStratOpt())
    return myteam
