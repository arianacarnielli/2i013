# -*- coding: utf-8 -*-
from soccersimulator import Strategy, SoccerAction, Vector2D
from .etat import Etat
from . import actions as act
import math


class RandomStrategy(Strategy):
	"""
	Random : Bouge et tire de façon aléatoire en continu.
	Classe en mode "Legacy"
	"""
	def __init__(self):
		Strategy.__init__(self, "Random")
    
	def compute_strategy(self, state, id_team, id_player):
		return SoccerAction(Vector2D.create_random(-1, 1), Vector2D.create_random(-1, 1))


class Fonceur(Strategy):
	"""
	Fonceur : Fonce vers la balle le plus vite possible, puis tire le plus fort possible vers les buts adverses.
	"""
	def __init__(self):
		Strategy.__init__(self, "Fonceur")

	def compute_strategy(self, state, id_team, id_player):
		etat = Etat(state, id_team, id_player)
		
		return SoccerAction(act.fonce(etat), act.tir_but(etat))
	

class Defenseur(Strategy):
	"""
	Défenseur : Se place en défense (son terrain) et éjecte la balle loin quand elle arrive.
	Va évidemment poursuivre les attaquants qui arrivent.
	"""
	def __init__(self):
		Strategy.__init__(self, "Défenseur")
	
	def compute_strategy(self, state, id_team, id_player):
		etat = Etat(state, id_team, id_player)
		
		return SoccerAction(act.defend(etat), act.degage(etat))
		

class Goal(Strategy):
	"""
	Goal : Se place devant ses buts, entre ses buts et la balle, et intercepte les tirs (en dégageant loin).
	Se déplace à peine.
	"""
	def __init__(self):
		Strategy.__init__(self, "Goal")
	
	def compute_strategy(self, state, id_team, id_player):
		#goal()
		#degage()
		etat = Etat(state, id_team, id_player)
		
	




