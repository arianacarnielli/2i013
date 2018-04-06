from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from module.strategies  import *


## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")
pyteam.add("Mil",FonceurStrategy()) #Strategie qui ne fait rien
thon.add("FonS",Milieu())   #Strategie aleatoire
pyteam.add("Def",Gardien())
thon.add("FonS",FonceurStrategy())

#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)
