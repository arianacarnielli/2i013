# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:48:29 2018

@author: 3525837
"""


from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator.settings import *
from soccersimulator import Strategy
from tools import ToolBox

import math


## Strategie aleatoire

class RandomStrategy(Strategy):
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
        
        loc_ball = state.ball.position
        loc_player = state.player_state(id_team, id_player).position
        
        if(loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS): 
            if(id_team == 1):
                loc_goal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
            else:
                loc_goal = Vector2D(0, GAME_HEIGHT/2)
            return SoccerAction(shoot = loc_goal - loc_player)
        else:
            return SoccerAction((loc_ball - loc_player)* maxPlayerAcceleration)
        
        
## Strategie shoot ball speed
        
class ShootBallSpeedStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la vitesse de la balle.
    """
    def __init__(self):
        Strategy.__init__(self,"ShootBallSpeed")
        
    def compute_strategy(self,state,id_team,id_player):
        
        loc_ball = state.ball.position
        loc_player = state.player_state(id_team, id_player).position
        vit_ball = state.ball.vitesse
        
        if(loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS): 
            if(id_team == 1):
                loc_goal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
            else:
                loc_goal = Vector2D(0, GAME_HEIGHT/2)
            return SoccerAction(shoot = loc_goal - loc_ball - vit_ball)
            
        else:
            return SoccerAction((loc_ball + vit_ball - loc_player) * maxPlayerAcceleration)


class ShootBallStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self):
        Strategy.__init__(self,"ShootBall")
        
    def compute_strategy(self,state,id_team,id_player):
        
        loc_ball = state.ball.position
        loc_player = state.player_state(id_team, id_player).position
        vit_ball = state.ball.vitesse
        
        if(loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS): 
            if(id_team == 1):
                loc_goal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
            else:
                loc_goal = Vector2D(0, GAME_HEIGHT/2)
                
            return SoccerAction(shoot = loc_goal - loc_ball - vit_ball)
            
        else:
            while vit_ball.norm > 1e-2:
                loc_ball += vit_ball
                vit_ball.norm = vit_ball.norm - ballBrakeSquare * vit_ball.norm ** 2 - ballBrakeConstant * vit_ball.norm
            
            return SoccerAction((loc_ball + vit_ball - loc_player) * maxPlayerAcceleration)



class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((id_player)*GAME_WIDTH,GAME_HEIGHT/2)-state.ball.position)

class FonceurFaible(Strategy):
    def __init__(self):
        Strategy.__init__(self,"FonceurFaible")
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player)   
        
        if(tools.PosBall().distance(tools.PosJoueur()) < PLAYER_RADIUS + BALL_RADIUS): 
            return SoccerAction(shoot = tools.VecPosGoal().norm_max(4.5))
        else:
            return SoccerAction((tools.PosBall() - tools.PosJoueur())* maxPlayerAcceleration)
                
        
        
        
class TesteStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Teste")
    def compute_strategy(self,state,id_team,id_player):
        
        tools = ToolBox(state,id_team,id_player)        
        
        if tools.CanShoot():
            return SoccerAction(shoot = tools.VecPosGoal())
        else:
            return SoccerAction(tools.VecPosBall(10)* maxPlayerAcceleration)
            

            
#class DefNaifStrategy(Strategy):
#    def __init__(self):
#        Strategy.__init__(self,"Teste")
#    def compute_strategy(self,state,id_team,id_player):
#        
#        tools = ToolBox(state,id_team,id_player)        
#        
#        if(id_team == 1):
#            if(tools.PosJoueur() )
#        
