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

        
        tol = module.ToolBox(state,idteam,idplayer)
        act = module.Action(tol)
        
        oth = tol.FindClosestBall(tol.PosBall())
        if (tol.CanShoot()) and me.vitesse.norm < 0.5:
            if (abs(me.position.norm - oth.position.norm) < settings.BALL_RADIUS * 20):
                return act.ShootPasse(oth.position)
            else:
                return act. ShootPasse(oth.position, acc = 0.2)
            
        vecposball = tol.VecPosBall()        
        if vecposball.norm<5:
            vecposball.norm=0.1
        return SoccerAction(acceleration=vecposball)



class Fonceur_test4(Strategy):
    """
    On essaye de se raprocher de la balle gris foncé la plus proche du but avant de la frapper avec plus de vitesse. Si la balle gris foncé est devant le joueur, if fait un shoot vers la cage.
    """
    def __init__(self):
        super(Fonceur_test4,self).__init__("test4")
    def compute_strategy(self,state,idteam,idplayer):
        ball = state.ball
        me = state.player_state(1,0)
        
        tol = module.ToolBox(state,idteam,idplayer)
        act = module.Action(tol)
        
        posGoal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        oth = tol.FindClosestBall(posGoal)

        if(tol.CanShoot()) and  me.vitesse.norm < 0.5:
            if(abs(me.position.norm - oth.position.norm) < settings.BALL_RADIUS * 10):
                if tol.ExisteBallDevant:
                    return act.ShootGoal()                
                else:
                    return act.ShootPasse(oth.position)
            else:
                return act.ShootPasse(oth.position, acc = 0.2)
            
        vecposball = tol.VecPosBall()        
        if vecposball.norm<5:
            vecposball.norm=0.1
        return SoccerAction(acceleration=vecposball)


class Fonceur_test5(Strategy):
    """
    L'idée de la stratégie est de viser non pas le centre de la balle, mais légèrement plus haut lorsque la balle se trouve au-dessus du but pour qu'elle aille vers le bas, 
    ou légèrement plus bas lorsqu'elle se trouve au-dessous pour qu'elle monte. 
    Le sens de "légèrement" est défini par le paramètre theta, qui ne peut pas être trop grand pour ne pas rater la balle.
    """
    def __init__(self):
        super(Fonceur_test5,self).__init__("test5")
    def compute_strategy(self,state,idteam,idplayer):
        ball = state.ball
        me = state.player_state(1,0)
        
        tol = module.ToolBox(state,idteam,idplayer)
        act = module.Action(tol)
        
        posGoal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        oth = tol.FindClosestBall(posGoal)

        vecBallToOth = oth.position - ball.position    
        vecBallToGoal = posGoal - ball.position
        theta = 0.01
        vecShoot = vecBallToOth * 10
        
        if(tol.CanShoot()) and  me.vitesse.norm < 0.5:
            if(abs(me.position.norm - oth.position.norm) > settings.BALL_RADIUS * 10):
                if vecBallToGoal.angle > vecBallToOth.angle:
                    vecShoot.angle = vecShoot.angle - theta
                    vecShoot = vecShoot + me.position
                    return act.ShootPasse(vecShoot, acc = 0.2)
                else:
                    vecShoot.angle = vecShoot.angle + theta
                    vecShoot = vecShoot + me.position
                    return act.ShootPasse(vecShoot, acc = 0.2)

            return act.ShootPasse(oth.position, acc = 0.5)
            
        vecposball = tol.VecPosBall()        
        if vecposball.norm<5:
            vecposball.norm=0.1
        return SoccerAction(acceleration=vecposball)




myt = SoccerTeam("teste")
myt.add("N",Fonceur_test5())
b = Billard(myt,type_game=2)
show_simu(b)

