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
        
    def ShootAtk(self):
        """
        Renvoie une SoccerAction de tir droit vers le champ adversaire.
        """
        return SoccerAction(shoot = self.tools.VecShoot())

    def ShootGoal(self, acc = 1):
        """
        Renvoie une SoccerAction de tir au but. Si acc n'est pas donne, le tir est fait avec l'acceleration maximale.
        """
        return SoccerAction(shoot = self.tools.VecPosGoal(acc * maxBallAcceleration))
        
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

        
    