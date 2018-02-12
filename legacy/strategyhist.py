# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 23:38:07 2018

@author: arian
"""

class RandomStrategy(Strategy):
    """
    Strategie aleatoire.
    """
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-0.5,0.5), Vector2D.create_random(-0.5,0.5))
              
    
class ShootBallSpeedStrategy(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la vitesse de la balle.
    """
    def __init__(self):
        Strategy.__init__(self,"ShootBallSpeed")
    def compute_strategy(self,state,id_team,id_player):
        comp = Comportement(state,id_team,id_player)
        return comp.ComShootSpeed(state,id_team,id_player)
        
        
        
class ShootBallStrategyTwoAccelerations(Strategy):
    """
    Strategie de tir vers le milieu du but que prend en consideration la position attendue de la balle.
    """
    def __init__(self, accFirst, accOthers):
        Strategy.__init__(self,"ShootBallTwoAccelerations")
        self.accFirst = accFirst
        self.accOthers = accOthers        
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        return comp.ComShootStrategyTwoAccelerations(state,id_team,id_player, self.accFirst, self.accOthers)
       

class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        return comp.ComFonceurStrategy(state,id_team,id_player)

class FonceurFaible(Strategy):
    def __init__(self):
        Strategy.__init__(self,"FonceurFaible")
    def compute_strategy(self,state,id_team,id_player):
        
        comp = Comportement(state,id_team,id_player)
        return comp.ComFonceurFaible(state,id_team,id_player)

            
    
    
    
    
    
    
 ###Comportements###
   
    def ComShootSpeed(self, state, id_team, id_player):
        
        act = Action(state,id_team,id_player)
        tools = ToolBox(state,id_team,id_player)  
        vit_ball = state.ball.vitesse
        
        if tools.CanShoot(): 
            return SoccerAction(shoot = act.VecPosGoal(maxBallAcceleration) - vit_ball)
        else:
            return SoccerAction(act.VecPosBall(1, maxPlayerAcceleration))
        
                  
 

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
    
     
    def ComFonceurStrategy(self, state, id_team, id_player):
        
        tools = ToolBox(state,id_team,id_player)
        return SoccerAction(tools.PosBall()-tools.PosJoueur(),Vector2D(tools.PosCage()-tools.PosBall())
    
    def ComFonceurFaible(self, state, id_team, id_player):
        
        tools = ToolBox(state,id_team,id_player)
        act = Action(state,id_team,id_player)
        
        if(tools.PosBall().distance(tools.PosJoueur()) < PLAYER_RADIUS + BALL_RADIUS): 
            return SoccerAction(shoot = act.VecPosGoal().norm_max(4.5))
        else:
            return SoccerAction((tools.PosBall() - tools.PosJoueur())* maxPlayerAcceleration)
            