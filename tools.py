# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:32:13 2018

@author: 3525837
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player, Ball
from soccersimulator.settings import *
from soccersimulator import Strategy

import math

class ToolBox(object):
    
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player

    def CanShoot(self):
        loc_ball = self.state.ball.position
        loc_player = self.state.player_state(self.id_team, self.id_player).position
        
        return loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS
        
    def VecPosGoal(self):
        if(self.id_team == 1):
            loc_goal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        else:
            loc_goal = Vector2D(0, GAME_HEIGHT/2)
        return loc_goal - self.state.player_state(self.id_team, self.id_player).position
        
    def VecPosBall(self, n):
        loc_ball = self.state.ball.position
        vit_ball = self.state.ball.vitesse
    
        ball_temp = Ball(loc_ball, vit_ball)
        while(n > 0):
            ball_temp.next(Vector2D(0,0))
            loc_ball = ball_temp.position         
            n = n - 1
    
        return loc_ball - self.state.player_state(self.id_team, self.id_player).position
        
    def VecShoot(self):
        if(self.id_team == 1):
            return Vector2D(angle = 0, norm = maxBallAcceleration)
        else:
            return Vector2D(angle = math.pi, norm = maxBallAcceleration)
            
    def PosJoueur(self):
          return self.state.player_state(self.id_team, self.id_player).position
          
    def PosBall(self):
        return self.state.ball.position
    
