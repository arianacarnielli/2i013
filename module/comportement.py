# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:48 2018

@author: 3525837
"""

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player
from soccersimulator.settings import *
from soccersimulator import Strategy

from .toolbox import *
from .action import *


import math


class Comportement(object):
    
    def __init__(self, action):
        self.action = action
        
    def ComShoot(self, acc = 1, vit = 1, n = 0):
        """
        Comportement de base de attaque.
        """
        if self.action.tools.CanShoot(): 
            return self.action.ShootGoal(acc)
        else:
            return self.action.RunToBall(vit, n)
 
    def ComDef(self,  acc = 1, vit = 1, n = 5):
        """
        Comportement de base de defense.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootAtk()
        
        if self.action.tools.EstDef(n):
            return self.action.RunToBall(vit,n)
        
        if self.action.tools.EstGoalDef():
            return SoccerAction()
        return self.action.RunToDefGoal()

#######pas prete######
    def ComPass(self):
        
              
        amis = self.action.tools.GetPosAmis   
        
        if self.action.tools.CanShoot():
            for idplayer in amis:
                if self.action.tools.CanPass(idplayer) and idplayer != self.action.tools.PosJoueur: 
                    return SoccerAction(shoot = self.action.tools.VecPosJoueur(idplayer, maxBallAcceleration))
            return SoccerAction(shoot = self.action.tools.VecPosGoal(maxBallAcceleration))
        return SoccerAction(self.action.tools.VecPosBall(0, maxPlayerAcceleration))
        
            
            
            
             