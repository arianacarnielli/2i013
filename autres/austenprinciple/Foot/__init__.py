# -*- coding: utf-8 -*-
from .strategies import Fonceur, Defenseur
from soccersimulator import SoccerTeam


def get_team(nb_players):
	"""
	Compose une équipe de <nb_players> joueurs, selon l'organisation souhaitée
	"""
	myteam = SoccerTeam(name = "Team Expert")
	
	if nb_players == 1:
		myteam.add("Scarlett", Fonceur())
	if nb_players == 2:
		myteam.add("Scarlett", Defenseur())
		myteam.add("soO", Fonceur())
	if nb_players == 4:
		myteam.add("Scarlett", Defenseur())
		myteam.add("soO", Fonceur())
		myteam.add("Zest", Fonceur())
		myteam.add("Dark", Fonceur())
	return myteam
	

def get_team_challenge(num):
	myteam = SoccerTeam(name="Team Expert")
	if num == 1:
		myteam.add("Joueur Chal " + str(num), Fonceur())
	return myteam


