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
    myteam = SoccerTeam(name="Pariana")
    if nb_players == 1:
        
        myteam.add("Messi", DribleIntelligent1v1Strat(accShoot = 0.9, accDrible = 0.5, vit = 1, n = 7, maxAngle = 1.46, tooFar = 0, rSurfBut = 50, AngleHyst = 0.13, alpha = 0.9))
    #self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/3, tooFar = 10*maxBallAcceleration, rSurfBut = 40, AngleHyst = math.pi/12)
    if nb_players == 2:
        #myteam.add("Joueur 1", ShootBallStratOpt(acc = 1))
        #myteam.add("Cafu", DefIntelligentStratOpt(p = 0.8))
        #myteam.add("RRRRONALDO", DribleStratOpt2(n = 18, accShoot = 0.25, maxAngle = math.pi/4, tooFar = 9*maxBallAcceleration))
        
        #myteam.add("Matuidi", DefIntelligentStratOpt(p = 0.9, n = 0, frac_p = 0.4))
        #myteam.add("Ronaldo", DribleStratOpt2(accShoot = 0.64, accDrible = 0.25, vit = 1, n = 0, maxAngle = 0.08, tooFar = 42, rSurfBut = 35, AngleHyst = 0.08))
        
        myteam.add("Ronaldo", DribleStratOpt2(accShoot = 0.9, accDrible = 0.25, vit = 1.0, n = 10, maxAngle = 1.06, tooFar = 53, rSurfBut = 45, AngleHyst = 0.07, distShoot = 50))
        myteam.add("Matuidi", DefIntelligentStratOpt(p = 0.9, n = 2, alpha = 0.6, distMin = 25, distMax = 54, maxAngle = 0.69, rayon = 15))
        
        #[accShoot, accDrible, vit, nDrible, maxAngle, tooFar, rSurfBut, AngleHyst, p, nDef, frac_p]

    if nb_players == 4:
        myteam.add("Messi", DribleStratOpt2(accShoot = 1.0, accDrible = 0.9, vit = 1.0, n = 5, maxAngle = 0.72, tooFar = 33, rSurfBut = 30, AngleHyst = 0.18, distShoot = 2))
        myteam.add("Matuidi", DefIntelligentStratOpt(p = 0.3, n = 1, alpha = 0.4, distMin = 14, distMax = 122, maxAngle = 1.43, rayon = 15))
        myteam.add("Romario", AtkIntelligentStratOpt(distShoot = 75, accShoot = 0.8, distMin = 2, distMax = 104, rayon = 13, alpha = 0.5))
        myteam.add("Neymar", DefIntelligentStratOpt(p = 1.3, n = 17, alpha = 0.7, distMin = 18, distMax = 67, maxAngle = 0.84, rayon = 25))
    return myteam	

def get_team_challenge(num):
    myteam = SoccerTeam(name="Brasil")
    if num == 1:
        myteam.add("Joueur Chal "+str(num),ShootBallStratOpt())
    return myteam
