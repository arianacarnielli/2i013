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
        myteam.add("RRRRONALDO", Drible1vs1StratOpt2(accShoot = 0.9, accDrible = 0.1, vit = 1, n = 18, maxAngle = 0.69, tooFar = 40, rSurfBut = 50, AngleHyst = 0.18))
    #self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/3, tooFar = 10*maxBallAcceleration, rSurfBut = 40, AngleHyst = math.pi/12)
    if nb_players == 2:
        #myteam.add("Joueur 1", ShootBallStratOpt(acc = 1))
#        myteam.add("Cafu", Def2StratOpt(p = 0.8))
#        myteam.add("RRRRONALDO", DribleStratOpt2(n = 18, accShoot = 0.25, maxAngle = math.pi/4, tooFar = 9*maxBallAcceleration))
        
        myteam.add("Cafu", Def2StratOpt(p = 0.8, n = 10, frac_p = 0.9))
        myteam.add("RRRRONALDO", DribleStratOpt2(accShoot = 0.4, accDrible = 0.9, vit = 1, n = 7, maxAngle = 0.08, tooFar = 42, rSurfBut = 35, AngleHyst = 0.08))
        #[accShoot, accDrible, vit, nDrible, maxAngle, tooFar, rSurfBut, AngleHyst, p, nDef, frac_p]

    if nb_players == 4:
        myteam.add("RRRRonaldo", DribleStratOpt2(n = 18, accShoot = 0.25, maxAngle = math.pi/4, tooFar = 9*maxBallAcceleration))
        myteam.add("Cafu",Def2StratOpt(p = 0.8))
        myteam.add("Ronaldinho", DribleStratOpt2(n = 18, accShoot = 0.25, maxAngle = math.pi/4, tooFar = 9*maxBallAcceleration))
        myteam.add("Taffarel",DefStratOpt(0.7))
    return myteam	

def get_team_challenge(num):
    myteam = SoccerTeam(name="Brasil")
    if num == 1:
        myteam.add("Joueur Chal "+str(num),ShootBallStratOpt())
    return myteam
