# -*- coding: utf-8 -*-
from soccersimulator import Strategy, SoccerAction, Vector2D
from .etat import Etat
from . import actions as act
import math


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
		

