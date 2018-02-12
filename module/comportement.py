# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:48 2018

@author: 3525837
"""

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player
from soccersimulator.settings import *
from soccersimulator import Strategy

from .toolbox import *
from .action import *


import math


class Comportement(object):
    
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    def ComShoot(self, state, id_team, id_player):
        
        tools = ToolBox(state,id_team,id_player)
        act = Action(state,id_team,id_player)
        
        if tools.CanShoot(): 
            return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration))
        else:
            return SoccerAction(act.VecPosBall(0, maxPlayerAcceleration))
            
    def ComShootSpeed(self, state, id_team, id_player):
        
        act = Action(state,id_team,id_player)
        tools = ToolBox(state,id_team,id_player)  
        vit_ball = state.ball.vitesse
        
        if tools.CanShoot(): 
            return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration) - vit_ball)
        else:
            return SoccerAction(act.VecPosBall(1, maxPlayerAcceleration))
            
    def ComShootStrategy(self, state, id_team, id_player, acc):
        self.acc = acc        
        tools = ToolBox(state,id_team,id_player)
        act = Action(state,id_team,id_player)

        if tools.CanShoot(): 
            return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration * self.acc))
        else:
            return SoccerAction(act.VecPosBall(30, maxPlayerAcceleration))  

    def ComShootStrategyTwoAccelerations(self, state, id_team, id_player, accFirst, accOthers):
        self.accFirst = accFirst
        self.accOthers = accOthers
        tools = ToolBox(state,id_team,id_player)
        act = Action(state,id_team,id_player)
        self.firstShoot = True
        if tools.CanShoot():
            if self.firstShoot:
                return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration * self.accFirst))
                self.firstShoot = False
            return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration * self.accOthers))
        else:
            return SoccerAction(act.VecPosBall(30, maxPlayerAcceleration))  
    
#    def ComFonceurStrategy(self, state, id_team, id_player):
#        
#        tools = ToolBox(state,id_team,id_player)
#        return SoccerAction(tools.PosBall()-tools.PosJoueur(),Vector2D(tools.PosCage()-tools.PosBall())
    
#    def ComFonceurFaible(self, state, id_team, id_player):
#        
#        tools = ToolBox(state,id_team,id_player)
#        act = Action(state,id_team,id_player)
#        
#        if(tools.PosBall().distance(tools.PosJoueur()) < PLAYER_RADIUS + BALL_RADIUS): 
#            return SoccerAction(shoot = act.VecPosGoal().norm_max(4.5))
#        else:
#            return SoccerAction((tools.PosBall() - tools.PosJoueur())* maxPlayerAcceleration)
#            
    def ComDefNaifStrategy(self, state, id_team, id_player):
        
        tools = ToolBox(state,id_team,id_player)
        act = Action(state,id_team,id_player)
        
        if tools.CanShoot():
            return SoccerAction(shoot = act.VecShoot())
        
        if tools.EstDef(10):
            return SoccerAction(act.VecPosBall(10, maxPlayerAcceleration))
        
        return SoccerAction(tools.PosCage() - tools.PosJoueur())

    def ComPassStrategy(self, state, id_team, id_player):
        
        tools = ToolBox(state,id_team,id_player)
        act = Action(state,id_team,id_player)
        amis = tools.get_amis()      
        
        if tools.CanShoot():
            for idplayer in amis:
                if tools.CanPass(idplayer) and idplayer != tools.PosJoueur(): 
                    return SoccerAction(shoot = act.VecPosJoueur(idplayer, maxBallAcceleration))
            return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration))
        return SoccerAction(act.VecPosBall(0, maxPlayerAcceleration))
        
            
            
            
             