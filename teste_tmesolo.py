# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:58:21 2018

@author: 3525837
"""

from soccersimulator import SoccerAction,Vector2D,settings ,SoccerTeam,Billard,show_simu,Strategy
import module
import math


class FonceurLent(Strategy):
    def __init__(self):
        super(FonceurLent,self).__init__("fonceur")
    def compute_strategy(self,state,idteam,idplayer):
        ball = state.ball
        me = state.player_state(1,0)
        oth = state.balls[0]
        shoot = (oth.position-ball.position)*100
        if (me.position.distance(ball.position)<(settings.BALL_RADIUS + settings.PLAYER_RADIUS)) and  me.vitesse.norm<0.5:
            return SoccerAction(shoot=shoot)
        acc = ball.position-me.position
        if acc.norm<5:
            acc.norm=0.1
        return SoccerAction(acceleration=acc)



class Fonceur_test1(Strategy):
    """
    Copie de la strategie donne mais avec mes fonctions auxiliaires.
    """
    def __init__(self):
        super(Fonceur_test1,self).__init__("test1")
    def compute_strategy(self,state,idteam,idplayer):
        ball = state.ball
        me = state.player_state(1,0)
        oth = state.balls[0]
        shoot = (oth.position-ball.position)*100
        
        tol = module.ToolBox(state,idteam,idplayer)
        act = module.Action(tol)
        
        if (tol.CanShoot()) and  me.vitesse.norm < 0.5:
            return act.ShootPasse(oth.position)
            
        vecposball = tol.VecPosBall()
        if vecposball.norm<5:
            vecposball.norm=0.1
        return SoccerAction(acceleration=vecposball)



class Fonceur_test2(Strategy):
    """
    On cherche a fraper la balle la plus proche. Il fonctionne donc pour le cas avec 2 balles. 
    """
    def __init__(self):
        super(Fonceur_test2,self).__init__("test2")
    def compute_strategy(self,state,idteam,idplayer):
        ball = state.ball
        me = state.player_state(1,0)
        
        tol = module.ToolBox(state,idteam,idplayer)
        act = module.Action(tol)
        
        oth = tol.FindClosestBall(tol.PosBall())
        
        if (tol.CanShoot()) and  me.vitesse.norm < 0.5:
            
            return act.ShootPasse(oth.position)
            
        vecposball = tol.VecPosBall()
        if vecposball.norm<5:
            vecposball.norm=0.1
        return SoccerAction(acceleration=vecposball)



class Fonceur_test3(Strategy):
    """
    On essaye de se raprocher de la balle gris foncé avant de la frapper avec plus de vitesse.
    """
    def __init__(self):
        super(Fonceur_test3,self).__init__("test3")
    def compute_strategy(self,state,idteam,idplayer):
        ball = state.ball
        me = state.player_state(1,0)
        alpha = math.pi/4
        
        tol = module.ToolBox(state,idteam,idplayer)
        act = module.Action(tol)
        
        oth = tol.FindClosestBall(tol.PosBall())
        
        if (tol.CanShoot()) and  me.vitesse.norm < 0.5:
            if (abs(me.position.norm - oth.position.norm) < settings.BALL_RADIUS * 20):
                return act.ShootPasse(oth.position)
            else:
                return act. ShootPasse(oth.position, acc = 0.1)
        vecposball = tol.VecPosBall()
        if vecposball.norm<5:
            vecposball.norm=0.1
        return SoccerAction(acceleration=vecposball)








myt = SoccerTeam("teste")
myt.add("N",Fonceur_test3())
b = Billard(myt,type_game=0)
show_simu(b)

