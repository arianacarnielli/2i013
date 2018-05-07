# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:58:21 2018

@author: 3525837
"""

from soccersimulator import SoccerAction,Vector2D,settings ,SoccerTeam,Billard,show_simu,Strategy
import module


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





myt = SoccerTeam("teste")
myt.add("N",Fonceur_test1())
b = Billard(myt,type_game=0)
show_simu(b)

