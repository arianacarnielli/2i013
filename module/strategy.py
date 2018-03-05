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
    
class DribleStrat(Strategy):
    """
    Strategie d'attaque avec drible.
    """
    def __init__(self):
        Strategy.__init__(self,"Def")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComDrible(accShoot = 0.25, accDrible = 0.25, maxAngle = math.pi/3, tooFar = 10*maxBallAcceleration)
        

class PassStrat(Strategy):
    """
    Strategie de passe entre deux joueurs.
    """
    def __init__(self, accPasse = 0.1, accShoot = 1, vit = 1, n = 4, tooClose = 100 * PLAYER_RADIUS):
        Strategy.__init__(self,"PassOpt")
        self.accPasse = accPasse
        self.accShoot = accShoot
        self.vit = vit
        self.n = n
        self.tooClose = tooClose
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComPass(accShoot = self.accShoot, vit = self.vit, n = self.n, tooClose = self.tooClose)


###############################################################################
### Strategies de teste  pour optimisation                                  ###
###############################################################################

class DefStratOpt(Strategy):
    """
    Strategie de defense de la cage, on peut tester combien de pas on essaie de predir la position de la balle et a partir de quand le defenseur doit sortir de la cage.
    """
    def __init__(self, p = 0.7, n = 3):
        Strategy.__init__(self,"DefOpt")
        self.p = p
        self.n = n
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComDef(p = self.p, n = self.n)        

        
class ShootBallStratOpt(Strategy):
    """
    Strategie de tir vers le milieu du but qui prend en consideration la position attendue de la balle, avec l'acceleration optimale pour 1 x 0.
    """
    def __init__(self, acc = 0.64, n = 4):
        Strategy.__init__(self, "ShootBallOptimal")
        self.acc = acc
        self.n = n
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComShoot(n = self.n, acc = self.acc)
        
class DribleStratOpt(Strategy):
    """
    Strategie d'attaque avec drible.
    """
    def __init__(self, accShoot = 0.25, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/3, tooFar = 10*maxBallAcceleration):
        Strategy.__init__(self,"Def")
        self.accShoot = accShoot
        self.accDrible = accDrible
        self.vit = vit
        self.n = n
        self.maxAngle = maxAngle
        self.tooFar = tooFar
        
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComDrible(accShoot = self.accShoot, accDrible = self.accDrible, vit = self.vit, n = self.n, maxAngle = self.maxAngle, tooFar = self.tooFar)
    
    
########## TESTE ############   
    
class DribleStratOpt2(Strategy):
    """
    Strategie d'attaque avec drible.
    """
    def __init__(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/3, tooFar = 10*maxBallAcceleration):
        Strategy.__init__(self,"Def")
        self.accShoot = accShoot
        self.accDrible = accDrible
        self.vit = vit
        self.n = n
        self.maxAngle = maxAngle
        self.tooFar = tooFar
        
        self.dernierdrible = None
        
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        comp.dernierdrible = self.dernierdrible
        act = comp.ComDrible2(accShoot = self.accShoot, accDrible = self.accDrible, vit = self.vit, n = self.n, maxAngle = self.maxAngle, tooFar = self.tooFar)
        self.dernierdrible = comp.dernierdrible
        return act
    
    
class Drible1vs1StratOpt2(Strategy):
    """
    Strategie d'attaque avec drible.
    """
    def __init__(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/3, tooFar = 10*maxBallAcceleration):
        Strategy.__init__(self,"Def")
        self.accShoot = accShoot
        self.accDrible = accDrible
        self.vit = vit
        self.n = n
        self.maxAngle = maxAngle
        self.tooFar = tooFar
        self.cpt = 0
        self.cpt2 = 0        
        self.dernierdrible = None
        
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        if state.get_score_team(1) + state.get_score_team(2) > self.cpt2:
            self.cpt2 = state.get_score_team(1) + state.get_score_team(2)
            self.cpt = 0
        self.cpt += 1

        comp.dernierdrible = self.dernierdrible
        act = comp.ComDrible21vs1(accShoot = self.accShoot, accDrible = self.accDrible, vit = self.vit, n = self.n, maxAngle = self.maxAngle, tooFar = self.tooFar, cpt = self.cpt)
        self.dernierdrible = comp.dernierdrible
        return act
    
class Def2StratOpt(Strategy):
    """
    Strategie de defense de la cage, on peut tester combien de pas on essaie de predir la position de la balle et a partir de quand le defenseur doit sortir de la cage.
    """
    def __init__(self, p = 0.7, n = 3, frac_p = 0.5):
        Strategy.__init__(self,"Def2Opt")
        self.p = p
        self.n = n
        self.frac_p = frac_p
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComDef2(p = self.p, n = self.n, frac_p = self.frac_p)       
    


                
class PassStratOpt(Strategy):
    """
    Strategie de passe entre deux joueurs.
    """
    def __init__(self, accPasse = 0.1, accShoot = 1, vit = 1, n = 4, tooClose = 100 * PLAYER_RADIUS):
        Strategy.__init__(self,"PassOpt")
        self.accPasse = accPasse
        self.accShoot = accShoot
        self.vit = vit
        self.n = n
        self.tooClose = tooClose
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(Action(ToolBox(state,id_team,id_player)))
        return comp.ComPass(accShoot = self.accShoot, vit = self.vit, n = self.n, tooClose = self.tooClose)
