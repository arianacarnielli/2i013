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
        Renvoie une SoccerAction de tir droit vers le champ adverse. Si acc n'est pas donne, le tir est fait avec l'acceleration maximale.
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
        Renvoie une SoccerAction de tir avec acceleration et angle donnés.
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
    
    def RunToDefense(self, pos_x = 0.5):
        """
        Renvoi une SoccerAction de courir vers une position defensive d'interception.
        """
        return SoccerAction(self.tools.VecDef(pos_x = pos_x, norm_acc = maxPlayerAcceleration))
        
    def RunToDefenseProp(self, alpha = 0.6):
        """
        Renvoi une SoccerAction de courir vers une position defensive d'interception.
        """
        return SoccerAction(self.tools.VecDefProportionnel(alpha = alpha, norm_acc = maxPlayerAcceleration))
    
    def RunToAtkProp(self, alpha = 0.6):
        """
        Renvoi une SoccerAction de courir vers une position d'attaque d'interception.
        """
        return SoccerAction(self.tools.VecAtkProportionnel(alpha = alpha, norm_acc = maxPlayerAcceleration))
    
    def RuntoAtaque(self, pos_x = 0.5):
        """
        Retourne une SoccerAction de courir vers une position de ataque.
        """
        return SoccerAction(self.tools.VecAtk(pos_x = pos_x, norm_acc = maxPlayerAcceleration))

        
    