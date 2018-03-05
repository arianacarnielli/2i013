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
    
    def __init__(self, action):
        self.action = action
        self.dernierdrible = None
                
    def ComShoot(self, acc = 1, vit = 1, n = 0):
        """
        Comportement de base de attaque.
        """
        if self.action.tools.CanShoot(): 
            return self.action.ShootGoal(acc)
        else:
            return self.action.RunToBall(vit, n)
 
    def ComDef(self, acc = 1, vit = 1, n = 0, p = 0.7):
        """
        Comportement de base de defense.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootAtk()
        
        if self.action.tools.EstDef(n, p):
            return self.action.RunToBall(vit,n)
        
        if self.action.tools.EstGoalDef():
            return SoccerAction()
        return self.action.RunToDefGoal()
    
    def ComDef2(self, acc = 1, vit = 1, n = 0, p = 0.7, frac_p = 0.5):
        """
        Comportement de defense.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootAtk()
        
        if self.action.tools.EstDef(n, p):
            return self.action.RunToBall(vit,n)

        return self.action.RunToDefense(p * frac_p)

    def ComDrible(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration):
        """
        Comportement de base d'attaque avec drible.
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
         
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                # Si l'autre joueur peut lui aussi tirer, essayer de tirer plus fort
                #if (self.action.tools.VecPosBall() - minPos).norm < PLAYER_RADIUS + BALL_RADIUS:
                #    return self.action.ShootGoal()
                
                # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                posGoal = self.action.tools.VecPosGoal()
                theta = minPos.angle - posGoal.angle
                if abs(theta) > maxAngle or minPos.norm > tooFar:
                    return self.action.ShootGoal(accShoot)
                elif theta > 0:
                    return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                else:
                    return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)   
        

    
    def ComDrible2(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration, rSurfBut = 40, AngleHyst = math.pi/12):
        """
        Comportement d'attaque avec drible, prend en consideration la position du joueur ennemi le plus proche devant et aussi si il est un gardien ou non, applique l'hysterese pour determiner l'angle de drible. 
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
            Posgoal = self.action.tools.PosCageAtk
            Posjoueur = self.action.tools.PosJoueur
            
            if abs(Posjoueur.x - Posgoal.x) < 5 and (Posjoueur.y <= Posgoal.y + GAME_GOAL_HEIGHT/2 and Posjoueur.y >= Posgoal.y - GAME_GOAL_HEIGHT/2) : 
                return self.action.ShootGoal(accShoot)
                        
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                # Si l'autre joueur peut lui aussi tirer, essayer de tirer plus fort
                if (self.action.tools.VecPosBall() - minPos).norm < PLAYER_RADIUS + BALL_RADIUS:
                    return self.action.ShootAtk()
                if self.action.tools.AdvAGardien() and self.action.tools.VecPosGoal().norm < rSurfBut:
                    return self.action.ShootCoinGoal()
                else:                    
                    # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                    posGoal = self.action.tools.VecPosGoal()
                    theta = minPos.angle - posGoal.angle
                    if abs(theta) > maxAngle or minPos.norm > tooFar:
                        return self.action.ShootGoal(accShoot)
                    elif theta > AngleHyst or (self.dernierdrible == "down" and abs(theta) <= AngleHyst):
                        self.dernierdrible = "down"
                        return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                    else:
                        self.dernierdrible = "up"
                        return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)
            
        
    def ComDrible21vs1(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration, rSurfBut = 50, AngleHyst = math.pi/12, cpt = 101):
        """
        Comportement d'attaque avec drible, prend en consideration la position du joueur ennemi le plus proche devant et aussi si il est un gardien ou non, applique l'hysterese pour determiner l'angle de drible. 
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
            Posgoal = self.action.tools.PosCageAtk
            Posjoueur = self.action.tools.PosJoueur
            
            if abs(Posjoueur.x - Posgoal.x) < 5 and (Posjoueur.y <= Posgoal.y + GAME_GOAL_HEIGHT/2 and Posjoueur.y >= Posgoal.y - GAME_GOAL_HEIGHT/2) : 
                return self.action.ShootGoal(accShoot)
                        
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                # Si l'autre joueur peut lui aussi tirer, essayer de tirer plus fort
                if (self.action.tools.VecPosBall() - minPos).norm < PLAYER_RADIUS + BALL_RADIUS:
                    return self.action.ShootAtk()
                if self.action.tools.VecPosGoal().norm < rSurfBut:
                    return self.action.ShootCoinGoal(accShoot)
                else:                    
                    # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                    posGoal = self.action.tools.VecPosGoal()
                    theta = minPos.angle - posGoal.angle
                    if abs(theta) > maxAngle or minPos.norm > tooFar:
                        return self.action.ShootGoal(accShoot)
                    elif theta > AngleHyst or (self.dernierdrible == "down" and abs(theta) <= AngleHyst):
                        self.dernierdrible = "down"
                        return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                    else:
                        self.dernierdrible = "up"
                        return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        elif cpt < 100 and abs(self.action.tools.PosBall().x - self.action.tools.PosJoueur.x) > 50:
            return
        else:    
            return self.action.RunToBall(vit, n)





    def ComPass(self, accPasse = 0.1, accShoot = 1, vit = 1, n = 4, tooClose = 100 * PLAYER_RADIUS):        
        
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAmisPlusProcheDevant()
            if not (minPos is None):
                Pos_joueur2 = minPos + self.action.tools.PosJoueur
                if minPos.norm > tooClose:
                    return self.action.ShootGoal(accShoot)
                else:
                    return self.action.ShootPasse(Pos_joueur2, accPasse)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)         
            
    



