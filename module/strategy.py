# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:48:29 2018

@author: 3525837
"""


from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player
from soccersimulator.settings import *
from soccersimulator import Strategy
#from tools import ToolBox
from .toolbox import *

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
        
        tools = ToolBox(state,id_team,id_player)   
        
        if tools.CanShoot(): 
            return SoccerAction(shoot = tools.VecPosGoal(maxBallAcceleration))
        else:
            return SoccerAction(tools.VecPosBall(0, maxPlayerAcceleration))
        
        
## Strategie shoot ball speed
        
class ShootBallSpeedStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la vitesse de la balle.
    """
    def __init__(self):
        Strategy.__init__(self,"ShootBallSpeed")
        
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player)  
        vit_ball = state.ball.vitesse
        
        if tools.CanShoot(): 
            return SoccerAction(shoot = tools.VecPosGoal(maxBallAcceleration) - vit_ball)
        else:
            return SoccerAction(tools.VecPosBall(1, maxPlayerAcceleration))
        
class ShootBallStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self, acc):
        Strategy.__init__(self,"ShootBall")
        self.acc = acc
        
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player)
         
        if tools.CanShoot(): 
            return SoccerAction(shoot = tools.VecPosGoal(maxBallAcceleration * self.acc))
        else:
            return SoccerAction(tools.VecPosBall(30, maxPlayerAcceleration))
        
class ShootBallStrategyTwoAccelerations(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self, accFirst, accOthers):
        Strategy.__init__(self,"ShootBallTwoAccelerations")
        self.accFirst = accFirst
        self.accOthers = accOthers
        self.firstShoot = True
        
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player)
         
        if tools.CanShoot():
            if self.firstShoot:
                return SoccerAction(shoot = tools.VecPosGoal(maxBallAcceleration * self.accFirst))
                self.firstShoot = False
            return SoccerAction(shoot = tools.VecPosGoal(maxBallAcceleration * self.accOther))
        else:
            return SoccerAction(tools.VecPosBall(30, maxPlayerAcceleration))
        
class ShootBallStrategyOptimal(ShootBallStrategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle, avec l'acceleration optimale.
    """
    def __init__(self):
        ShootBallStrategy.__init__(self,acc = 0.64)

class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((id_team)*GAME_WIDTH,GAME_HEIGHT/2)-state.ball.position)

class FonceurFaible(Strategy):
    def __init__(self):
        Strategy.__init__(self,"FonceurFaible")
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player)   
        
        if(tools.PosBall().distance(tools.PosJoueur()) < PLAYER_RADIUS + BALL_RADIUS): 
            return SoccerAction(shoot = tools.VecPosGoal().norm_max(4.5))
        else:
            return SoccerAction((tools.PosBall() - tools.PosJoueur())* maxPlayerAcceleration)

            
class DefNaifStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"DefNaif")
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player) 
        
        if tools.CanShoot():
            return SoccerAction(shoot = tools.VecShoot())
        
        if tools.EstDef(10):
            return SoccerAction(tools.VecPosBall(10, maxPlayerAcceleration))
        
        return SoccerAction(tools.PosCage() - tools.PosJoueur())
        
        