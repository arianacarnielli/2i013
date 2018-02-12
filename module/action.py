# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:07:35 2018

@author: 3525837
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player, Ball
from soccersimulator.settings import *
from soccersimulator import Strategy

import math

from .toolbox import *


class Action(object):
    
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player

   # @staticmethod
    def VecPosGoal(self, norm_acc = None):
        """
        retourne le vecteur du joueur au milieu du but. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        tools = ToolBox(self.state,self.id_team,self.id_player)               
        
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
                
        tools = ToolBox(self.state,self.id_team,self.id_player)   
        
        loc_ball = tools.PosBall(n)
    
        vec_ball = loc_ball - self.state.player_state(self.id_team, self.id_player).position
        
        if norm_acc != None:
            vec_ball.norm = norm_acc
            
        return vec_ball
        
        
    def VecShoot(self,norm_acc = maxBallAcceleration):
        """
        retourne un vecteur d'acceleration vers le champ opposé. Si norm_acc n'est pas donnée la norme du vecteur est definie comme maxBallAcceleration.
        """
        
        return  Vector2D(angle = (1 - self.id_team) * math.pi, norm = norm_acc)
        
    def VecPosJoueur(self, idplayer2, norm_acc = None):
        """
        retourne le vecteur du joueur à un autre. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        tools = ToolBox(self.state,self.id_team,self.id_player) 

        loc_player = tools.PosJoueur()
        vec_player = idplayer2 - loc_player 
        if norm_acc != None:
            vec_player.norm = norm_acc
            
        return vec_player