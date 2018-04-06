from soccersimulator import ChallengeFonceurButeur, SoccerTeam,show_simu
from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from module.strategie import Fonceur
from module.strategie import RandomStrategy
from module.strategie import Defenseur
from module.strategie import Bon_joueur_1v1

team = SoccerTeam("RandomEquipe")
team.add("RandomJoueur",Fonceur())

challenge = ChallengeFonceurButeur(team,max_but=20)
show_simu(challenge)
print("temps moyen : ",challenge.stats_score, "\nliste des temps",challenge.resultats)
