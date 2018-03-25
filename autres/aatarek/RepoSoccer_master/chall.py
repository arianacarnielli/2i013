from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from prog.strategies import *


## Creation d'une equipe
myteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")

#myteam.add("Joueur 1",defense())
#myteam.add("Joueur 2",stratAttente())
#myteam.add("Joueur 3",stratAttente())
myteam.add("Joueur 4",defense2())

thon.add("ThonPlayer",stratAttente())   #Strategie aleatoire
thon.add("ThonPlayer2",defense())   #Strategie aleatoire
#thon.add("ThonPlayer3",defense2())

#Creation d'une partie
simu = Simulation(myteam,thon)
#Jouer et afficher la partie
show_simu(simu)
