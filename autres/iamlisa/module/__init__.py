from .strategy import Fonceur3Strategy,DefenseurStrategy
from soccersimulator import *

def get_team(nb_players):
	myteam = SoccerTeam(name="MaTeam")
	if nb_players == 1:
		myteam.add("Joueur " ,Fonceur3Strategy())
	if nb_players == 2:
		myteam.add("Joueur 1", Fonceur3Strategy())
		myteam.add("Joueur 2", DefenseurStrategy())
	if nb_players == 4:
		myteam.add("Joueur 1",Fonceur3Strategy())
		myteam.add("Joueur 2",Fonceur3Strategy())
		myteam.add("Joueur 3",Fonceur3Strategy())
		myteam.add("Joueur 4",Fonceur3Strategy())
	return myteam	

def get_team_challenge(num):
	myteam = SoccerTeam(name="MaTeamChallenge")
	if num == 1:
		myteam.add("Joueur Chal "+str(num),Fonceur3Strategy())
	return myteam
