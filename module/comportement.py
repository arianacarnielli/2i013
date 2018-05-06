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
        self.position_ennemi_x = self.action.tools.PosAdvPlusProcheDeLaBalle.x
        self.position_ennemi_y = self.action.tools.PosAdvPlusProcheDeLaBalle.y
        
###############################################################################
### Comportements simples pour l'aprentissage de l'IA                       ###
###############################################################################
             
    def ComShootSimple(self, acc = 1, vit = 1, n = 5):
        """
        Comportement de base de attaque.
        """
        if self.action.tools.CanShoot(): 
            return self.action.ShootGoal(acc)
        else:
            return self.action.RunToBall(vit, n)
 
    def ComGardienSimple(self, acc = 1, vit = 1, n = 5, p = 0.7):
        """
        Comportement de base de gardien.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootAtk()
        
        if self.action.tools.EstDef(n, p):
            return self.action.RunToBall(vit,n)
        
        if self.action.tools.EstGoalDef():
            return SoccerAction()
        return self.action.RunToDefGoal()
    
    
    def ComDefSimple(self, acc = 1, vit = 1, n = 5, p = 0.7, frac_p = 0.5):
        """
        Comportement de base de defense.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootAtk()
        
        if self.action.tools.EstDef(n, p):
            return self.action.RunToBall(vit,n)

        return self.action.RunToDefense(p * frac_p)

    def ComDribleSimple(self, accShoot = 0.64, accDrible = 0.15, vit = 1, n = 4, maxAngle = math.pi/4, tooFar = 8*maxBallAcceleration):
        """
        Comportement de base d'attaque avec drible.
        """       
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
         
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                
                # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                posGoal = self.action.tools.VecPosGoal()
                if self.action.tools.id_team == 1:
                    theta = minPos.angle - posGoal.angle
                else:
                    minPos.x = -minPos.x
                    posGoal.x = -posGoal.x
                    theta = minPos.angle - posGoal.angle
                    minPos.x = -minPos.x
                    posGoal.x = -posGoal.x

                if abs(theta) > maxAngle or minPos.norm > tooFar:
                    return self.action.ShootGoal(accShoot)
                elif (theta > 0 and self.action.tools.id_team == 1) or (theta <= 0 and self.action.tools.id_team == 2) :
                    return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                else:
                    return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)   
        
        
    def ComPassSimple(self, accPasse = 0.25, accShoot = 1, vit = 1, n = 4):        
        """
        Comportement de base de passe.
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAmisPlusProche()
            if not (minPos is None):
                Pos_joueur2 = minPos + self.action.tools.PosJoueur
   
                return self.action.ShootPasse(Pos_joueur2, accPasse)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)  

        
    def ComAtkSimple(self, acc = 1, pos_x = 0.5, p = 0.5, n = 0, vit = 1):
        """
        Comportement de base de Romário.
        """
        if self.action.tools.CanShoot():
            return self.action.ShootGoal(acc)
        
        if self.action.tools.EstAtk(n, p):
            return self.action.RunToBall(vit,n)

        else:     
            return self.action.RuntoAtaque(pos_x)
            
       
###############################################################################
### Comportements                                                           ###
###############################################################################
             
                
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
    
    def ComAtkIntelligent(self, distShoot = 50, accShoot = 0.64, distMin = 10, distMax = 60, rayon = 15, alpha = 0.6):
        """
        Comportement d'ataque.
        """
        my_pos = self.action.tools.PosJoueur
        if self.action.tools.CanShoot():
            if abs(self.action.tools.VecPosGoal().x) < distShoot:
                return self.action.ShootGoal(acc = accShoot)
            vec_ami = self.action.tools.VecPosAmisPlusProcheDevant()
            if vec_ami is not None:
                if vec_ami.norm >= distMin and vec_ami.norm <= distMax and not self.action.tools.ExistAdvProcheAmi(vec_ami + my_pos, rayon):
                    return self.action.ShootPasse(vec_ami + my_pos, acc = vec_ami.norm/maxBallAcceleration)
            return self.action.ShootGoal(acc = accShoot)
        if self.action.tools.IsCloserToBallThanAll():
            return self.action.RunToBall()
        return self.action.RunToAtkProp(alpha)

    def ComDefIntelligent(self, acc = 1, vit = 1, n = 0, p = 0.7, alpha = 0.6, distMin = 10, distMax = 60, maxAngle = math.pi/6, rayon = 15):
        """
        Comportement de defense.
        """
        my_pos = self.action.tools.PosJoueur
        if self.action.tools.CanShoot():
            vec_ami = self.action.tools.VecPosAmisPlusProcheDevant()
            if vec_ami is not None:
                if vec_ami.norm >= distMin and vec_ami.norm <= distMax and not self.action.tools.ExistAdvProcheAmi(vec_ami + my_pos, rayon):
                    return self.action.ShootPasse(vec_ami + my_pos, acc = vec_ami.norm/maxBallAcceleration)
            
            vec_adv = self.action.tools.VecPosAdvPlusProcheDevant()
            if vec_adv is not None:
                vec_goal = self.action.tools.VecPosGoal()
                if self.action.tools.id_team == 1:
                    theta = vec_adv.angle - vec_goal.angle
                else:
                    vec_adv.x = -vec_adv.x
                    vec_goal.x = -vec_goal.x
                    theta = vec_adv.angle - vec_goal.angle
                    vec_adv.x = -vec_adv.x
                    vec_goal.x = -vec_goal.x
                if abs(theta) > maxAngle:
                    return self.action.ShootGoal()
                if (theta > 0 and self.action.tools.id_team == 1) or (theta <= 0 and self.action.tools.id_team ==2):
                    return self.action.ShootAngle(vec_adv.angle - maxAngle)
                return self.action.ShootAngle(vec_adv.angle + maxAngle)
            return self.action.ShootGoal()
        
        if self.action.tools.EstDef(n, p):
#            if self.action.tools.VecPosAdvPlusProcheDeLaBalle().norm + 5 < self.action.tools.VecPosBall().norm:
#                return self.action.RunToDefenseProp(alpha)
            return self.action.RunToBall(vit,n)

        return self.action.RunToDefenseProp(alpha)
        
    def ComDrible(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration):
        """
        Comportement de base d'attaque avec drible.
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
         
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                
                # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                posGoal = self.action.tools.VecPosGoal()
                if self.action.tools.id_team == 1:
                    theta = minPos.angle - posGoal.angle
                else:
                    minPos.x = -minPos.x
                    posGoal.x = -posGoal.x
                    theta = minPos.angle - posGoal.angle
                    minPos.x = -minPos.x
                    posGoal.x = -posGoal.x

                if abs(theta) > maxAngle or minPos.norm > tooFar:
                    return self.action.ShootGoal(accShoot)
                elif (theta > 0 and self.action.tools.id_team == 1) or (theta <= 0 and self.action.tools.id_team == 2) :
                    return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                else:
                    return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        else:
            return self.action.RunToBall(vit, n)  
        
    
    def ComDrible2(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration, rSurfBut = 40, AngleHyst = math.pi/12, distShoot = 50):
        """
        Comportement d'attaque avec drible, prend en consideration la position du joueur ennemi le plus proche devant et aussi s'il est un gardien ou non, applique l'hysterese pour determiner l'angle de drible. 
        """
        
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
            vecGoal = self.action.tools.VecPosGoal()
            
            if abs(vecGoal.x) < distShoot:
                return self.action.ShootGoal(accShoot)

            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                # Si l'autre joueur peut lui aussi tirer, essayer de tirer plus fort
                if (self.action.tools.VecPosBall() - minPos).norm < PLAYER_RADIUS + BALL_RADIUS:
                    return self.action.ShootAtk()
                if self.action.tools.AdvAGardien() and vecGoal.norm < rSurfBut:
                    return self.action.ShootCoinGoal()
                else:                    
                    # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                    if self.action.tools.id_team == 1:
                        theta = minPos.angle - vecGoal.angle
                    else:
                        minPos.x = -minPos.x
                        vecGoal.x = -vecGoal.x
                        theta = minPos.angle - vecGoal.angle
                        minPos.x = -minPos.x
                        vecGoal.x = -vecGoal.x
                    if abs(theta) > maxAngle or minPos.norm > tooFar:
                        return self.action.ShootGoal(accShoot)
                    elif theta > AngleHyst or (self.dernierdrible == "down" and abs(theta) <= AngleHyst):
                        self.dernierdrible = "down"
                        if self.action.tools.id_team == 1:
                            return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                        else:
                            return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
                    else:
                        self.dernierdrible = "up"
                        if self.action.tools.id_team == 1:
                            return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
                        else:
                            return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
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
            
            
    def ComDribleIntelligent1v1(self, accShoot = 0.64, accDrible = 0.25, vit = 1, n = 4, maxAngle = math.pi/6, tooFar = 5*maxBallAcceleration, rSurfBut = 50, AngleHyst = math.pi/12, alpha = 0.6):
        """
        Comportement d'attaque avec drible, prend en consideration la position du joueur ennemi le plus proche devant et aussi si il est un gardien ou non, applique l'hysterese pour determiner l'angle de drible. 
        """
        if self.action.tools.CanShoot():
            minPos = self.action.tools.VecPosAdvPlusProcheDevant()
            vecGoal = self.action.tools.VecPosGoal()
            # S'il y a un joueur entre moi et mon but
            if not (minPos is None):
                # Si l'autre joueur peut lui aussi tirer, essayer de tirer plus fort
                if (self.action.tools.VecPosBall() - minPos).norm < PLAYER_RADIUS + BALL_RADIUS:
                    return self.action.ShootAtk()
                if self.action.tools.AdvAGardien() and vecGoal.norm < rSurfBut:
                    return self.action.ShootCoinGoal()
                else:                    
                    # Si l'autre est un peu plus loin (mais pas trop), on essaie de le dribler
                    if self.action.tools.id_team == 1:
                        theta = minPos.angle - vecGoal.angle
                    else:
                        minPos.x = -minPos.x
                        vecGoal.x = -vecGoal.x
                        theta = minPos.angle - vecGoal.angle
                        minPos.x = -minPos.x
                        vecGoal.x = -vecGoal.x
                    if abs(theta) > maxAngle or minPos.norm > tooFar:
                        return self.action.ShootGoal(accShoot)
                    elif theta > AngleHyst or (self.dernierdrible == "down" and abs(theta) <= AngleHyst):
                        self.dernierdrible = "down"
                        if self.action.tools.id_team == 1:
                            return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
                        else:
                            return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
                    else:
                        self.dernierdrible = "up"
                        if self.action.tools.id_team == 1:
                            return self.action.ShootAngle(minPos.angle + maxAngle, accDrible)
                        else:
                            return self.action.ShootAngle(minPos.angle - maxAngle, accDrible)
            else:
                return self.action.ShootGoal(accShoot)
        
        elif self.position_ennemi_x == self.action.tools.PosAdvPlusProcheDeLaBalle.x and self.position_ennemi_y == self.action.tools.PosAdvPlusProcheDeLaBalle.y:
                self.position_ennemi_x = self.action.tools.PosAdvPlusProcheDeLaBalle.x
                self.position_ennemi_y = self.action.tools.PosAdvPlusProcheDeLaBalle.y
                return
        elif not self.action.tools.IsCloserToBall() and not self.action.tools.EstDef(p = 0.75): 
            self.position_ennemi_x = self.action.tools.PosAdvPlusProcheDeLaBalle.x
            self.position_ennemi_y = self.action.tools.PosAdvPlusProcheDeLaBalle.y
            return self.action.RunToDefenseProp(alpha)
        else:    
            return self.action.RunToBall(vit, n)  




    def ComPass(self, accPasse = 0.25, accShoot = 1, vit = 1, n = 4, tooClose = 100 * PLAYER_RADIUS):        
        
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
            
  

