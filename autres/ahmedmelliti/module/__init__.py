#from .strategies import RandomStrategy
#from .strategies import *
from .strategies  import *
from soccersimulator import SoccerTeam

def get_team(nb_players):
	myteam = SoccerTeam(name="MaTeam")
    #for i in range(nb_players):
    #    myteam.add("Joueur "+str(i) ,FonceurStrategy())
	if nb_players==1:
		myteam.add("Joueur "+str(0) ,FonceurStrategy())
	if nb_players==2:
		myteam.add("Joueur "+str(0) ,Defenseur())
		myteam.add("Joueur "+str(1) ,Milieu())			    
	return myteam	

def get_team_challenge(num):
	myteam = SoccerTeam(name="MaTeamChallenge")
	if num == 1:
		myteam.add("Joueur Chal "+str(num),FonceurStrategy())
	return myteam
