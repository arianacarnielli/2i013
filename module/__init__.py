# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:29:15 2018

@author: 3525837
"""
from .action import *
from .toolbox import *
from .strategy import *
from .comportement import *
    
    
def get_team(nb_players):
	myteam = SoccerTeam(name="Brasil")
	if nb_players == 1:
		myteam.add("Joueur " ,ShootStrat())
	if nb_players == 2:
		myteam.add("Joueur 1", ShootStrat())
		myteam.add("Joueur 2", DefStrat())
	if nb_players == 4:
		myteam.add("Joueur 1",ShootStrat())
		myteam.add("Joueur 2",DefStrat())
		myteam.add("Joueur 3",PassStrat())
		myteam.add("Joueur 4",DefStrat())
	return myteam	

def get_team_challenge(num):
	myteam = SoccerTeam(name="Brasil")
	if num == 1:
		myteam.add("Joueur Chal "+str(num),ShootStrat())
	return myteam
