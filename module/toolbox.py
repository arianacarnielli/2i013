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
        """
        determine si le joueur est a la proximite du ballon.
        """
        loc_ball = self.state.ball.position
        loc_player = self.state.player_state(self.id_team, self.id_player).position
        
        return loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS
    
        
    def VecPosGoal(self, norm_acc = None):
        """
        retourne le vecteur du joueur au milieu du but. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        if(self.id_team == 1):
            loc_goal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        else:
            loc_goal = Vector2D(0, GAME_HEIGHT/2)
        vec_goal = loc_goal - self.state.player_state(self.id_team, self.id_player).position
        if norm_acc != None:
            vec_goal.norm = norm_acc
        return vec_goal
        
        
    def VecPosBall(self, n = 0, norm_acc = None):
        """
        retourne le vecteur du joueur a la position prevu du ballon en n etapes. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        loc_ball = self.PosBall(n)
    
        vec_ball = loc_ball - self.state.player_state(self.id_team, self.id_player).position
        
        if norm_acc != None:
            vec_ball.norm = norm_acc
            
        return vec_ball
        
        
    def VecShoot(self,norm_acc = maxBallAcceleration):
        """
        retourne un vecteur d'acceleration vers le champ opposé. Si norm_acc n'est pas donnée la norme du vecteur est definie comme maxBallAcceleration.
        """
        
        return  Vector2D(angle = (1 - self.id_team) * math.pi, norm = norm_acc)

            
    def PosJoueur(self):
        """
        retourne le vecteur position du joueur.
        """
        return self.state.player_state(self.id_team, self.id_player).position
          
    def PosBall(self, n = 0):
        """
        retourne le vecteur position du ballon position prevu du ballon en n etapes.
        """

        loc_ball = self.state.ball.position
        vit_ball = self.state.ball.vitesse

        ball_temp = Ball(loc_ball, vit_ball)

        while(n > 0):
            ball_temp.next(Vector2D(0,0))
            loc_ball = ball_temp.position         
            n = n - 1        

        return loc_ball
    
    def PosCage(self):
        """
        retourne le vecteur position du milieu de la cage du joueur.
        """
        if(self.id_team == 0):
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
            
        return Vector2D(0, GAME_HEIGHT/2)
    
    def EstDef(self, n = 0):
        """
        retourne True si le ballon est dans le champs defensif d'un joueur en n etapes.
        """
        loc_ball = self.PosBall(n)
        
        if (self.PosCage().x == 0):    
            return GAME_WIDTH/4 > loc_ball.x
        return GAME_WIDTH/4 <= loc_ball.x