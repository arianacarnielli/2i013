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
 
    def ComDef(self, acc = 1, vit = 1, n = 0, p = 0.7):
        """
        Comportement de base de defense.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootAtk()
        
        if self.action.tools.EstDef(n, p):
            return self.action.RunToBall(vit,n)
        
        if self.action.tools.EstGoalDef():
            return SoccerAction()
        return self.action.RunToDefGoal()

    def ComDrible(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration):
        """
        Comportement de base d'attaque avec drible.
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                # Si l'autre joueur peut lui aussi tirer, essayer de tirer plus fort
                #if (self.action.tools.VecPosBall() - minPos).norm < PLAYER_RADIUS + BALL_RADIUS:
                #    return self.action.ShootGoal()
                
                # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                posGoal = self.action.tools.VecPosGoal()
                theta = minPos.angle - posGoal.angle
                if abs(theta) > maxAngle or minPos.norm > tooFar:
                    return self.action.ShootGoal(accShoot)
                elif theta > 0:
                    return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                else:
                    return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)

#######pas prete######
    def ComPass(self):
        
              
        amis = self.action.tools.GetPosAmis   
        
        if self.action.tools.CanShoot():
            for idplayer in amis:
                if self.action.tools.CanPass(idplayer) and idplayer != self.action.tools.PosJoueur: 
                    return SoccerAction(shoot = self.action.tools.VecPosJoueur(idplayer, maxBallAcceleration))
            return SoccerAction(shoot = self.action.tools.VecPosGoal(maxBallAcceleration))
        return SoccerAction(self.action.tools.VecPosBall(0, maxPlayerAcceleration))
        
            
            
            
             