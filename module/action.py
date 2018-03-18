# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:07:35 2018

@author: 3525837
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player, Ball
from soccersimulator.settings import *

import math

from .toolbox import *


class Action(object):
    
    def __init__(self, tools):
        self.tools = tools
        
        
###############################################################################
### Shoots                                                                  ###
###############################################################################
        
    def ShootAtk(self, acc = 1):
        """
        Renvoie une SoccerAction de tir droit vers le champ adversaire. Si acc n'est pas donne, le tir est fait avec l'acceleration maximale.
        """
        return SoccerAction(self.tools.VecPosBall(0, maxPlayerAcceleration), shoot = self.tools.VecShoot(acc * maxBallAcceleration))

    def ShootGoal(self, acc = 1):
        """
        Renvoie une SoccerAction de tir au but. Si acc n'est pas donne, le tir est fait avec l'acceleration maximale.
        """
        return SoccerAction(shoot = self.tools.VecPosGoal(acc * maxBallAcceleration))
    
    def ShootCoinGoal(self, acc = 1):
        """
         Renvoie une SoccerAction de tir au coin plus proche du but. Si acc n'est pas donne, le tir est fait avec l'acceleration maximale.
        """
        return SoccerAction(shoot = self.tools.VecPosCoinGoal(acc * maxBallAcceleration))
        
    def ShootPasse(self, loc_player2, acc = 1):
        """
        Renvoie une SoccerAction de tir droit vers un autre joueur. Si acc n'est pas donne, le tir est fait avec l'acceleration maximale.
        """
        return SoccerAction(shoot = self.tools.VecPosJoueur(loc_player2, acc * maxBallAcceleration))
    
    def ShootAngle(self, angle = 0, acc = 1):
        """
        Renvoie une SoccerAction de tir avec acceleration donnée et angle par rapport à sa direction d'attaque.
        """
        return SoccerAction(shoot = self.tools.VecAngle(angle, acc * maxBallAcceleration))
    
###############################################################################
### Run                                                                     ###
###############################################################################
        
    def RunToBall(self, vit = 1, n = 0):
        """
        Renvoie une SoocerAction de courir vers la position prevue du ballon en n etapes. Vit determine l'acceleration du joueur. 
        """
        return SoccerAction(self.tools.VecPosBall(n, vit * maxPlayerAcceleration))
        
        
    def RunToDefGoal(self):
        """
        Renvoie une SoocerAction de courir vers la cage de defense.
        """
        return SoccerAction(self.tools.PosCageDef - self.tools.PosJoueur)
    
    def RunToDefense(self, pos_x):
        """
        Renvoi une SoccerAction de courir vers une position defensive d'interception.
        """
        return SoccerAction(self.tools.PosDefense(pos_x) - self.tools.PosJoueur)

        
    