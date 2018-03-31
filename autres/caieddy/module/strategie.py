from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from .Outil import Outil
from soccersimulator.settings import *

## STRATEGY

class idiot1(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.idiot1()

class idiot2(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.idiot2()

class idiot3(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.idiot3()

class Fonceur_brain(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.fonceur_brain(id_team)


class Fonceur(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.attaque_fonceur(id_team)


class RandomStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")

	def compute_strategy(self,state,id_team,id_player):
		return SoccerAction(Vector2D.create_random(10,10),0)
		

class Defenseur(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.defense(id_team)


class Defenseur_2v2(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.defense_2v2(id_team)

	
class Bon_joueur_1v1(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.dribbler_1v1(id_team)


class Bon_joueur_2v2(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")	

	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		if (outil.ball_devant_player(id_team)):
			return outil.fonceur_brain(id_team)
		if (outil.recuperation_ball_pret()):
			return outil.fonceur_brain(id_team)
		return outil.revenir_posi_counter(id_team)




##OPTIMIZATION

class Fonceur_brain_opti(Strategy):
	def __init__(self, cst_dribble_A=10, cst_dribble_B=40):
		Strategy.__init__(self,"Random")	
		self.cst_dribble_A = cst_dribble_A
		self.cst_dribble_B = cst_dribble_B

	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player, cst_dribble_A=self.cst_dribble_A, cst_dribble_B=self.cst_dribble_B)
		return outil.fonceur_brain(id_team)


class Defenseur_2v2_opti(Strategy):
	def __init__(self,cst_defense=0,cst_prediction=0.6):
		Strategy.__init__(self,"Random")
		self.cst_defense = cst_defense
		self.cst_prediction = cst_prediction

	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player, cst_defense=self.cst_defense, cst_prediction=self.cst_prediction)
		return outil.defense_2v2(id_team)
			
			







			
