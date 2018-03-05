from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
from .fonctions_strategies import *
from .actions_simples import *
from .etat import Etat
import math

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-0.5,0.5),Vector2D.create_random(-0.5,0.5))

class ZigzagStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Zigzag")
	def compute_strategy(self,state,id_team,id_player):
		return zigzag(state,id_team,id_player)

class DefenseStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Defenseur")
	def compute_strategy(self,state,id_team,id_player):
		return defense(state,id_team,id_player)

class AttaqueStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Attaquant")
	def compute_strategy(self,state,id_team,id_player):
		return attaquant(state,id_team,id_player)

class FonceurStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur")
	def compute_strategy(self,state,id_team,id_player):
		e=Etat(state,id_team,id_player)
		dist=e.distballe()
		if (dist <= PLAYER_RADIUS+BALL_RADIUS):
			return SoccerAction(dirballe(e,2),dirgoal(e,3.65))
		else:
			return SoccerAction(dirballe(e,2))

