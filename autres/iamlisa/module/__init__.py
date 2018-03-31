from .strategy import Fonceur3Strategy, DefenseurStrategy, Fonceur3_modifStrategy, Defenseur_topStrategy, Defenseur_downStrategy, Fonceur3_downStrategy, Fonceur3_topStrategy
from soccersimulator import SoccerTeam

def get_team(nb_players):
	myteam = SoccerTeam(name="MaTeam")
	if nb_players == 1:
		myteam.add("Joueur " ,Fonceur3Strategy())
	if nb_players == 2:
		myteam.add("Joueur 1", Fonceur3_modifStrategy())
		myteam.add("Joueur 2", DefenseurStrategy())
	if nb_players == 4:
		myteam.add("Joueur 1",Defenseur_downStrategy())
		myteam.add("Joueur 2",Defenseur_topStrategy())
		myteam.add("Joueur 3",Fonceur3_downStrategy())
		myteam.add("Joueur 4",Fonceur3_topStrategy())
	return myteam	

def get_team_challenge(num):
	myteam = SoccerTeam(name="MaTeamChallenge")
	if num == 1:
		myteam.add("Joueur Chal "+str(num),Fonceur3Strategy())
	return myteam
