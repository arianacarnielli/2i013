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
      
class ShootStrat(Strategy):
    """
    Strategie de tir direct vers le milieu du but.
    """
    def __init__(self):
        Strategy.__init__(self,"Shoot")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComShoot()
        
        
class ShootBallPrevStrat(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self):
        Strategy.__init__(self,"ShootBall")   
        self.n = 30
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComShoot(n = self.n)
 
        
class ShootBallOptimalStrat(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle, avec l'acceleration optimale pour 1 x 0.
    """
    def __init__(self):
        Strategy.__init__(self, "ShootBallOptimal")
        self.acc = 0.64
        self.n = 30
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComShoot(n = self.n, acc = self.acc)
 

class DefStrat(Strategy):
    """
    Strategie de defense de la cage.
    """
    def __init__(self):
        Strategy.__init__(self,"Def")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComDef()
        

####pas pret#####
class PassStrat(Strategy):
    """
    Strategie de passe entre deux joueurs.
    """
    def __init__(self):
        Strategy.__init__(self,"Pass")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComPass()


###############################################################################
### Strategies de teste  pour optimisation                                  ###
###############################################################################

class DefStratOpt(Strategy):
    """
    Strategie de defense de la cage, on peut tester combien de pas on essaie de predir la position de la balle et a partir de quand le defenseur doit sortir de la cage.
    """
    def __init__(self, p = 0.5, n = 3):
        Strategy.__init__(self,"DefOpt")
        self.p = p
        self.n = n
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComDef(p = self.p, n = self.n)        

        
class ShootBallOptimalStrat(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle, avec l'acceleration optimale pour 1 x 0.
    """
    def __init__(self):
        Strategy.__init__(self, "ShootBallOptimal")
        self.acc = 0.64
        self.n = 30
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComShoot(n = self.n, acc = self.acc)
        