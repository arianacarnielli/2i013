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

class FonceurStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur Lambda")
	def compute_strategy(self,state,id_team,id_player):
		return fonceur_defaut(state,id_team,id_player, 4)

class DefenseStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Defenseur")
	def compute_strategy(self,state,id_team,id_player):
		return defense(state,id_team,id_player, 3.5)

class AttaqueStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Attaquant")
	def compute_strategy(self,state,id_team,id_player):
		return attaque(state,id_team,id_player, 4)

