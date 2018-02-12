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
        
####Booleans###

    def CanShoot(self):
        """
        determine si le joueur est a la proximite du ballon.
        """
        loc_ball = self.state.ball.position
        loc_player = self.state.player_state(self.id_team, self.id_player).position
        
        return loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS
        
    
    def EstDef(self, n = 0):
        """
        retourne True si le ballon est dans le champs defensif d'un joueur en n etapes.
        """
        loc_ball = self.PosBall(n)
        
        if (self.PosCage().x == 0):    
            return loc_ball.x < GAME_WIDTH/4
        return loc_ball.x >= 3*GAME_WIDTH/4
        
###Getters###
            
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
        if(self.id_team == 1):
            return Vector2D(0, GAME_HEIGHT/2)
            
        return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        
    def CanPass(self, idplayer2):
        """
        determine si deux joueurs sont a proximite.
        """
        loc_player1 = self.PosJoueur()
        loc_player2 = idplayer2
        
        return loc_player1.distance(loc_player2) < PLAYER_RADIUS*70 and loc_player1.distance(loc_player2) > PLAYER_RADIUS*30


    def get_amis(self):
        
        amis = [self.state.player_state(idteam, idplayer).position for idteam, idplayer in self.state.players if idteam == self.id_team]
        return amis

