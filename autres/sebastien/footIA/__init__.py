from soccersimulator import SoccerTeam
from .strats import *
from .tools import *

def get_team(nb_players):
        myteam = SoccerTeam(name="Barca")
        if nb_players == 1:
                myteam.add("dribleursebouss" ,DribleStrategy())
        if nb_players == 2:
                myteam.add("attaquant " ,AttStrategy())
                myteam.add("defenseur",DefStrategy())
        if nb_players == 4:
                myteam.add("Versatile 1",MultipurposeStrategy())
                myteam.add("Goal",GoalStrategy())
                myteam.add("Versatile 2",MultipurposeStrategy())
                myteam.add("DribleurNaif",DribleStrategy())
        return myteam

def get_team_challenge(num):
        myteam = SoccerTeam(name="SebOuss")
        if num == 1:
                myteam.add("Joueur Chal"+str(num),RandomStrategy())
        return myteam
