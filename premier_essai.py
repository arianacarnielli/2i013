# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:18:41 2018

@author: 3525837
"""

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator.settings import PLAYER_RADIUS, BALL_RADIUS
from soccersimulator import Strategy

import math


## Strategie aleatoire
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-0.5,0.5), Vector2D.create_random(-0.5,0.5))
        
        
# Strategie shoot
        
class ShootStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Shoot")
    def compute_strategy(self,state,id_team,id_player):
        
        loc_ball = state.ball.position
        loc_player = state.player_state(id_team, id_player).position
        
        if(loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS): 
            if(id_team == 1):
                return SoccerAction(shoot =  )
            else:
                return SoccerAction(shoot = )
        else:
            return SoccerAction(loc_ball - loc_player)



## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")
pyteam.add("PyPlayer",ShootStrategy()) #Strategie qui ne fait rien
thon.add("ThonPlayer",ShootStrategy())   #Strategie aleatoire

#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)