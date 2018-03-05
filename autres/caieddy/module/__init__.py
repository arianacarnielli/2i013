import sys

from soccersimulator import SoccerTeam
from .strategie import Fonceur
from .strategie import Defenseur
from .strategie import Defenseur_2v2
from .strategie import Bon_joueur_1v1
from .strategie import Bon_joueur_2v2
from .Outil import Outil
from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from .Outil import Outil
from soccersimulator.settings import *

def get_team(nb_players):
	myteam = SoccerTeam(name="Vous Êtes Où dans le classement? En dessou de nous ;_;")
	if nb_players == 1:
		myteam.add("Le meilleur" ,Bon_joueur_1v1())
	if nb_players == 2:
		myteam.add("The Best",Bon_joueur_2v2())
		myteam.add("The Wall",Defenseur_2v2())
	if nb_players == 4:
		myteam.add("Joueur 1",Defenseur_2v2())
		myteam.add("Joueur 2",Fonceur())
		myteam.add("Joueur 3",Bon_joueur_2v2())
		myteam.add("Joueur 4",Defenseur_2v2())
	return myteam	

def get_team_challenge(num):
	myteam = SoccerTeam(name="MaTeamChallenge")
	if num == 1:
		myteam.add("Joueur Chal "+str(num),Fonceur())
	return myteam
