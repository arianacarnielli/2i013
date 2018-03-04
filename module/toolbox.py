# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:32:13 2018

@author: 3525837
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Player, Ball
from soccersimulator.settings import *

import math



class ToolBox(object):
    
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
###############################################################################
### Booleans                                                                ###
###############################################################################

    def CanShoot(self):
        """
        determine si le joueur est a la proximite du ballon.
        """
        loc_ball = self.state.ball.position
        loc_player = self.state.player_state(self.id_team, self.id_player).position
        
        return loc_ball.distance(loc_player) < PLAYER_RADIUS + BALL_RADIUS
        
    
    def EstDef(self, n = 0, p = 1):
        """
        retourne True si le ballon est dans le champs defensif d'un joueur en n etapes. p = 1 signale le x du milieu du champs, p = 0 signale le x de la cage de defense. 
        """
        loc_ball = self.PosBall(n)
        
        if (self.PosCageDef.x == 0):    
            return loc_ball.x < p*(GAME_WIDTH/2)
        return loc_ball.x >= GAME_WIDTH *(1 -p/2)
    
    
    def CanPass(self, loc_player2):
        """
        determine si une passe peut etre fait entre deux joueurs.
        """
        loc_player1 = self.PosJoueur
        
        return loc_player1.distance(loc_player2) < PLAYER_RADIUS*70 and loc_player1.distance(loc_player2) > PLAYER_RADIUS*30

    def IsCloserToBall(self, n = 0):
        """
        determine si le joueur courant est plus proche du ballon que tous les joueurs adversaires.
        """
        posAdversaires = self.GetPosAdversaires()
        posBall = self.PosBall(n)
        return self.PosJoueur.distance(posBall) < min([posAdv.distance(posBall) for posAdv in posAdversaires])

    def EstGoalDef(self):
        """
        determine si le joueur courant est dans sa cage de defense.
        """
        loc_player = self.PosJoueur
        loc_goal = self.PosCageDef
        
        return loc_player.y >= (GAME_HEIGHT - GAME_GOAL_HEIGHT)/2 and loc_player.y <= (GAME_HEIGHT + GAME_GOAL_HEIGHT)/2 and abs(loc_player.x - loc_goal.x) < PLAYER_RADIUS*2
    
    def EstDevant(self, loc_player2):
        """
        determine si le joueur 2 est devant le joueur actuel.
        """
        loc_player1 = self.PosJoueur
        return (loc_player2.x > loc_player1.x and self.id_team == 1) or (loc_player2.x < loc_player1.x and self.id_team == 2)
    
    def ExisteAdversaireDevant(self):
        """
        determine s'il existe un joueur adversaire devant le joueur actuel.
        """
        advPos = self.GetPosAdversaires
        for pos in advPos:
            if self.EstDevant(pos):
                return True
        return False
        
    def ExisteAmiDevant(self):
        """
        determine s'il existe un joueur ami devant le joueur actuel.
        """
        amisPos = self.GetPosAmis
        for pos in amisPos:
            if self.EstDevant(pos):
                return True
        return False

    def AdvAGardien(self):
        """
        determine s'il y a un joueur adversaire a la cage (donc un joueur qui acte comme gardien).
        """
        PosGoal = self.PosCageAtk
        advPos = self.GetPosAdversaires
        for adv in advPos:
            if abs(adv.x - PosGoal.x) < 3 and adv.y <= PosGoal.y + GAME_GOAL_HEIGHT/2 and adv.y >= PosGoal.y - GAME_GOAL_HEIGHT/2:
                return True
        return False
    
        
###############################################################################        
### Getters                                                                 ###
###############################################################################
          
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
    
    def PosDefense(self, pos_x = 0.5):
        """
        retourne le vecteur donnant une position defensive pour intercepter la balle si l'ennemi tire droit vers le but.
        """
        VecBallGoalDef = self.PosCageDef - self.PosBall()
        x = pos_x * GAME_WIDTH/2
        y = x * VecBallGoalDef.y/VecBallGoalDef.x
        if(self.id_team == 2):
            x = GAME_WIDTH - x
        y = abs(y)
        if self.PosBall().y > GAME_HEIGHT/2:
            y = y + GAME_HEIGHT/2
        else:
            y = GAME_HEIGHT/2 - y
        return Vector2D(x, y)
    
    @property
    def PosJoueur(self):
        """
        retourne le vecteur position du joueur.
        """
        return self.state.player_state(self.id_team, self.id_player).position
        
    @property    
    def PosCageDef(self):
        """
        retourne le vecteur position du milieu de la cage de defense du joueur courant.
        """
        if(self.id_team == 1):
            return Vector2D(0, GAME_HEIGHT/2)
            
        return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
    
    @property    
    def PosCageAtk(self):
        """
        retourne le vecteur position du milieu de la cage d'attaque du joueur courant.
        """
        if(self.id_team == 1):
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
            
        return Vector2D(0, GAME_HEIGHT/2)
        
    @property
    def GetPosAmis(self):
        """
        retourne une liste avec les positions des joueurs de l'equipe courant, sans le joueur courant. 
        """
        return [self.state.player_state(idteam, idplayer).position for idteam, idplayer in self.state.players if idteam == self.id_team and idplayer != self.id_player]
    
    @property    
    def GetPosAdversaires(self):
        """
        retourne une liste avec les positions des joueurs de l'equipe adversaire. 
        """
        return [self.state.player_state(idteam, idplayer).position for idteam, idplayer in self.state.players if idteam != self.id_team]

###############################################################################
### Vecteurs                                                                ###
###############################################################################

    def VecPosGoal(self, norm_acc = None):
        """
        retourne le vecteur du joueur au milieu du but. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        loc_goal = self.PosCageAtk
        vec_goal = loc_goal - self.PosJoueur
        if not (norm_acc is None):
            vec_goal.norm = norm_acc
        return vec_goal
    
    def VecPosCoinGoal(self, norm_acc = None):
        """
        retourne le vecteur du joueur au coin du but le plus proche de lui. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        loc_goal = self.PosCageAtk
        if self.PosJoueur.y > GAME_HEIGHT/2:
            loc_goal.y += GAME_GOAL_HEIGHT/2
        else:
            loc_goal.y -= GAME_GOAL_HEIGHT/2
            
        vec_goal = loc_goal - self.PosJoueur
        if not (norm_acc is None):
            vec_goal.norm = norm_acc
        return vec_goal
        
        
    def VecPosBall(self, n = 0, norm_acc = None):
        """
        retourne le vecteur du joueur a la position prevu du ballon en n etapes. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """       
        loc_ball = self.PosBall(n)
        vec_ball = loc_ball - self.PosJoueur
        if not (norm_acc is None):
            vec_ball.norm = norm_acc  
        return vec_ball
        
    def VecShoot(self,norm_acc = maxBallAcceleration):
        """
        retourne un vecteur d'acceleration vers le champ opposé. Si norm_acc n'est pas donnée la norme du vecteur est definie comme maxBallAcceleration.
        """
        return Vector2D(angle = (1 - self.id_team) * math.pi, norm = norm_acc)
        
    def VecPosJoueur(self, loc_player2, norm_acc = None):
        """
        retourne le vecteur du joueur à un autre. Si norm_acc est donnéé, le vecteur renvoye est normalise a cette valeur.
        """
        loc_player = self.PosJoueur
        vec_player = loc_player2 - loc_player 
        if not (norm_acc is None):
            vec_player.norm = norm_acc
        return vec_player

    def VecAngle(self, angle = 0, norm_acc = maxBallAcceleration):
        """
        retourne un vecteur d'acceleration avec l'angle passé en paramètre.
        """
        return Vector2D(angle = angle, norm = norm_acc)
 
    def VecPosAdvPlusProcheDevant(self, norm_acc = None):
        """
        retourne le vecteur du joueur actuel au joueur adversaire le plus proche devant lui. Retourne None s'il n'y a pas d'adversaire devant.
        """
        advPos = self.GetPosAdversaires
        minPos = None
        for pos in advPos:
            if self.EstDevant(pos):
                newVec = self.VecPosJoueur(pos)
                if minPos is None or newVec.norm < minPos.norm:
                    minPos = newVec
        if not (minPos is None) and not (norm_acc is None):
            minPos.norm = norm_acc
        return minPos
        
    def VecPosAmisPlusProcheDevant(self, norm_acc = None):
        """
        retourne le vecteur du joueur actuel au joueur ami le plus proche devant lui. Retourne None s'il n'y a pas d'adversaire devant.
        """
        amisPos = self.GetPosAmis
        minPos = None
        for pos in amisPos:
            if self.EstDevant(pos):
                newVec = self.VecPosJoueur(pos)
                if minPos is None or newVec.norm < minPos.norm:
                    minPos = newVec
        if not (minPos is None) and not (norm_acc is None):
            minPos.norm = norm_acc
        return minPos
