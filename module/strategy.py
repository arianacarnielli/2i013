# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:48:29 2018

@author: 3525837
"""


from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player
from soccersimulator.settings import *
from soccersimulator import Strategy

from .toolbox import *
from .action import *
from .comportement import *

import math


## Strategie aleatoire

class RandomStrategy(Strategy):
    """
    Strategie aleatoire.
    """
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-0.5,0.5), Vector2D.create_random(-0.5,0.5))
              
## Strategie shoot
        
class ShootStrategy(Strategy):
    """
    Strategie de tir direct vers le milieu du but.
    """
    def __init__(self):
        Strategy.__init__(self,"Shoot")
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        
        return comp.ComShoot(state,id_team,id_player)
        
        
## Strategie shoot ball speed
        
class ShootBallSpeedStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la vitesse de la balle.
    """
    def __init__(self):
        Strategy.__init__(self,"ShootBallSpeed")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(state,id_team,id_player)
        return comp.ComShootSpeed(state,id_team,id_player)
        
        
class ShootBallStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self, acc):
        Strategy.__init__(self,"ShootBall")
        self.acc = acc
        
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        return comp.ComShootStrategy(state,id_team,id_player,self.acc)
        
        
class ShootBallStrategyTwoAccelerations(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self, accFirst, accOthers):
        Strategy.__init__(self,"ShootBallTwoAccelerations")
        self.accFirst = accFirst
        self.accOthers = accOthers

        
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        return comp.ComShootStrategyTwoAccelerations(state,id_team,id_player, self.accFirst, self.accOthers)
        
        
#class ShootBallStrategyOptimal(ShootBallStrategy):
#    """
#    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle, avec l'acceleration optimale.
#    """
#    def __init__(self):
 #       ShootBallStrategy.__init__(self,acc = 0.64)

#class FonceurStrategy(Strategy):
#    def __init__(self):
#        Strategy.__init__(self,"Fonceur")
#    def compute_strategy(self,state,id_team,id_player):
#        
#        comp = Comportement(state,id_team,id_player)
#        return comp.ComFonceurStrategy(state,id_team,id_player)

#class FonceurFaible(Strategy):
#    def __init__(self):
#        Strategy.__init__(self,"FonceurFaible")
#    def compute_strategy(self,state,id_team,id_player):
#        
#        comp = Comportement(state,id_team,id_player)
#        return comp.ComFonceurFaible(state,id_team,id_player)

            
class DefNaifStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"DefNaif")
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        return comp.ComDefNaifStrategy(state,id_team,id_player)

class PassStrategy(Strategy):
    """
    Strategie de passe entre deux joueurs.
    """
    def __init__(self):
        Strategy.__init__(self,"Pass")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(state,id_team,id_player)
        return comp.ComPassStrategy(state,id_team,id_player)
        
        
        