from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from .Outil import Outil
from soccersimulator.settings import *

## Fonceur sur la balle
class Fonceur_brain_Test(Strategy):
	def __init__(self, CONSTANTE_A=10, CONSTANTE_B=40):
		Strategy.__init__(self,"Random")	
		self.CONSTANTE_A = CONSTANTE_A
		self.CONSTANTE_B = CONSTANTE_B
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player, CONSTANTE_A=self.CONSTANTE_A, CONSTANTE_B=self.CONSTANTE_B)
		return outil.fonceur_brain(id_team)

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


class FonceurTest(Strategy):
	def __init__(self, force=1):
		Strategy.__init__(self,"Random")
		self.force = force
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player, force=self.force)
		return outil.attaque_fonceur(id_team)

## Strategie aleatoire
class RandomStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	def compute_strategy(self,state,id_team,id_player):
		return SoccerAction(Vector2D.create_random(10,10),0)
		
## Defenseur
class Defenseur(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.defense(id_team)

## Defenseur_2v2
class Defenseur_2v2(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.defense_2v2(id_team)

## Defenseur_2v2_opti
#class Defenseur_2v2_opti(Strategy):
	#def __init__(self,CONSTANTE_A=0,CONSTANTE_B=1):
	#	Strategy.__init__(self,"Random")
	#	self.CONSTANTE_A = CONSTANTE_A
	#	self.CONSTANTE_B = CONSTANTE_B	
	#def compute_strategy(self,state,id_team,id_player):
	#	outil = Outil(state, id_team, id_player, CONSTANTE_A=self.CONSTANTE_A, CONSTANTE_B=self.CONSTANTE_B)
	#	return outil.defense_2v2(id_team)
			
			
			
## Bon_joueur_1v1
	
class Bon_joueur_1v1(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		return outil.dribbler_1v1(id_team)


## Bon_joueur_2v2
class Bon_joueur_2v2(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")	
	def compute_strategy(self,state,id_team,id_player):
		outil = Outil(state, id_team, id_player)
		if (outil.ball_devant_player(id_team)):
			return outil.dribbler_1v1(id_team)
		if (outil.recuperation_ball_pret()):
			return outil.dribbler_1v1(id_team)
		return outil.revenir_posi_counter(id_team)













			