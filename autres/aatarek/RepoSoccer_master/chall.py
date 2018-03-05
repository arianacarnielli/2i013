from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from strategies  import *


## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")

pyteam.add("PyPlayer",stratAttente()) #Strategie qui ne fait rien
pyteam.add("PyPlayer2",stratAttente()) #Strategie qui ne fait rien

thon.add("ThonPlayer",flemme())   #Strategie aleatoire
thon.add("ThonPlayer2",flemme())   #Strategie aleatoire

#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)
