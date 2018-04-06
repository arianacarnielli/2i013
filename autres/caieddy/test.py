from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from module.strategie import Fonceur
from module.strategie import Fonceur_brain
from module.strategie import RandomStrategy
from module.strategie import Defenseur
from module.strategie import Defenseur_2v2
from module.strategie import Defenseur_2v2_opti
from module.strategie import Bon_joueur_1v1
from module.strategie import Bon_joueur_2v2
from module.strategie import *



## Creation d'une equipe
pyteam = SoccerTeam(name="Je suis nul et je suis devant vous -_- ???? ?PROBLEM?")
thon = SoccerTeam(name="ThonTeam")


#pyteam.add("PyPlayer",Bon_joueur_2v2())
pyteam.add("PyPlayer",Defenseur_2v2())

thon.add("ThonPlayer",Fonceur_brain())
#thon.add("ThonPlayer",Defenseur_2v2())
















#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)

