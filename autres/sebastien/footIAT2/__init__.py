from soccersimulator import SoccerTeam
from .strats import *
from .tools import *

def get_team(nb_players):
	myteam = SoccerTeam(name="SebOuss")
	if nb_players == 1:

		myteam.add("fonceur" ,FonceurStrategy())

		
	if nb_players == 2:
		myteam.add("defenseur 1", DefStrategy())
		myteam.add("attaaunt", AttStrategy())
	if nb_players == 4:
		myteam.add("defenseur",DefStrategy())
		myteam.add("attaquant",AttStrategy())
		myteam.add("defenseur",DefStrategy())
		myteam.add("attaquant",AttStrategy())
	return myteam	

def get_team_challenge(num):

	myteam = SoccerTeam(name="SebOuss")
	if num == 1:
		myteam.add("Joueur Chal"+str(num),RandomStrategy())

	return myteam
