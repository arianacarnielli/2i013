# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:18:41 2018

@author: 3525837
"""

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator.settings import *
from soccersimulator import Strategy

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
            return SoccerAction(loc_ball - loc_player)
        
        
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
            return SoccerAction(loc_ball + vit_ball - loc_player)


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
            
            return SoccerAction(loc_ball - loc_player)





## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")
pyteam.add("PyPlayer",ShootBallStrategy())
thon.add("ThonPlayer",ShootStrategy())   #Strategie aleatoire0.

#Creation d'une partie
simu = Simulation(pyteam,thon)


#Jouer et afficher la partie
show_simu(simu)
